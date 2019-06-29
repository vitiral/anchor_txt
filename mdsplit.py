import re

KEY_TEXT = "text"
KEY_LEVEL = "level"
KEY_ANCHOR = "anchor"
KEY_CODE_IDENTIFIER = "iden"

HEADER_RE = re.compile(r'''
(?P<level>^\#+)         # level
\s*
(?P<text>.*?)           # text
(?:\s*\{\#              # opening anchor
    (?P<anchor>.*?)
\})?                    # closing anchor
\s*$
'''
, re.VERBOSE)

FENCE_RE = re.compile(r'^```(?P<iden>[^`]*)$')
EMPTY_RE = re.compile(r'^\s*$')

BLOCK_MAYBE_RE = re.compile(r'    [^ ].*$')


class Header(object):
    TYPE = "HEADER"

    def __init__(self, raw, level, anchor, text):
        assert isinstance(raw, list)
        assert isinstance(level, int)
        if anchor is not None:
            assert isinstance(anchor, (str, unicode))
        assert isinstance(text, list)
        self.raw = raw
        self.level = level
        self.anchor = anchor
        self.text = text

    def to_dict(self):
        return {
            "type": self.TYPE,
            "raw": self.raw,
            "anchor": self.anchor,
            "text": self.text,
        }

    def __repr__(self):
        return "Header({} text={}, anchor={})".format(self.level, repr(self.text), repr(self.anchor))

    def _tuple(self):
        return (self.raw, self.anchor, self.text)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._tuple() == other._tuple()


class Code(object):
    TYPE = "CODE"

    def __init__(self, raw, identifier, text):
        self.raw = raw
        self.identifier = identifier
        self.text = text

    def to_dict(self):
        return {
            "type": self.TYPE,
            "raw": self.raw,
            "identifier": self.identifier,
            "text": self.text,
        }

    def __repr__(self):
        return "Code(identifier={}, text={})".format(repr(self.identifier), repr(self.text[:100]))

    def _tuple(self):
        return (self.raw, self.identifier, self.text)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._tuple() == other._tuple()



class CodeBuilder(object):
    def __init__(self, raw_start, is_indented, identifier):
        self.is_indented = is_indented
        self.identifier = identifier
        self.raw_lines = [raw_start]
        self.text_lines = []

    def append(self, line):
        self.raw_lines.append(line)
        if self.is_indented:
            self.text_lines.append(line[4:])
        else:
            self.text_lines.append(line)

    def append_raw(self, raw_line):
        self.raw_lines.append(raw_line)

    def build(self):
        return Code(
            raw=self.raw_lines,
            identifier=self.identifier,
            text=self.text)


class Text(object):
    TYPE = "TEXT"

    def __init__(self, raw=None):
        if raw is None:
            raw = []

        assert isinstance(raw, list)
        self.raw = raw

    def append(self, line):
        self.raw.append(line)

    def to_dict(self):
        return {
            "type": self.TYPE,
            "raw": self.raw,
        }

    def __repr__(self):
        return "Text(raw={})".format(repr(self.raw[:10]))

    def _tuple(self):
        return (self.raw,)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._tuple() == other._tuple()


def from_dict(dct):
    if dct['type'] == 'TEXT':
        return Text(raw=dct['raw'])
    elif dct['type'] == 'HEADER':
        return Header(raw=dct['raw'], level=dct['level'], anchor=dct['anchor'], text=dct['text'])
    else:
        raise TypeError("Invalid dct: {}", dct)


def split(md_text):
    lines = md_text.split('\n')

    tokens = []

    code_builder = None

    for line in lines:
        line = unicode(line)
        # Code indented
        mat = BLOCK_MAYBE_RE.match(line)
        if (mat
                and code_builder is None
                and tokens and isinstance(tokens[-1], Text)
                and tokens[-1].raw[-1] == ""):
            code_builder = CodeBuilder(line, True, None)
            continue

        if code_builder and code_builder.is_indented:
            if mat or EMPTY_RE.match(line):
                # append an indented or empty line
                code_builder.append(line)
                continue
            else:
                tokens.append(code_builder.build())
                code_builder = None
                # don't continue, let other lexers look at line

        # Code fence (```)
        mat = FENCE_RE.match(line)
        if mat:
            if code_builder:
                # we already have a code builder, so this must be ending the code section
                code_builder.append_raw(line)
                tokens.append(code_builder.build())
                code_builder = None
                continue
            else:
                code_builder = CodeBuilder(line, False, mat[KEY_CODE_IDENTIFIER])
                continue

        # Headers
        mat = HEADER_RE.match(line)
        if mat is not None:
            groups = mat.groupdict()
            header = Header(
                raw=[mat.group(0)],
                level=len(groups[KEY_LEVEL]),
                anchor=groups[KEY_ANCHOR],
                text=[groups[KEY_TEXT]],
            )

            if (tokens
                    and isinstance(tokens[-1], Header)
                    and tokens[-1].level == header.level):
                # If the last line was a header of the same level, merge them
                tokens[-1].text.extend(header.text)
                tokens[-1].raw.extend(header.raw)
                if header.anchor is not None:
                    tokens[-1].anchor = header.anchor
            else:
                tokens.append(header)
            continue

        if tokens and isinstance(tokens[-1], Text):
            tokens[-1].append(line)
        else:
            tokens.append(Text([line]))

    if code_builder:
        tokens.append(code_builder.build())

    return tokens

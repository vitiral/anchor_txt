# Splits the file and pull out attributes and sections

import os
import re

import yaml

from . import utils
from . import mdsplit

ATTR_IDENTIFIER_RE = re.compile(r"^yaml.*\s@$")
ATTR_INLINE_RE = re.compile(r"`@(.*)`")


class Section(object):
    def __init__(self, parent, header, attributes, sections, contents):
        self._parent = parent
        self.header = header
        self.attributes = attributes
        self.sections = section
        self.contents = contents

    @classmethod
    def new(cls, parent, header):
        return cls(
            parent=parent,
            header=header,
            attributes={},
            sections=[],
            contents=[])

    @classmethod
    def from_md(cls, filename, md_text):
        components = mdsplit.split(md_text)
        root = cls.new(None, None)
        curent_section = root

        for cmt in components:
            if isinstance(cmt, mdsplit.Header):
                new_section = Section(cmt)
                current_section.append_section(new_section)
                current_section = new_section
            elif isinstance(cmt, mdsplit.Code):
                if cmt.identifier and ATTR_IDENTIFIER_RE.match(cmt.identifier):
                    current_section.update_attributes(yaml.load(cmt.text))
                current_section.contents.append(cmt)
            else:
                assert isinstance(cmt, mdsplit.Text)
                # TODO: check for inline attributes
                current_section.contents.append(cmt)

        return root

    @classmethod
    def from_md_path(cls, path):
        filename = os.path.basename(path)
        with open(path) as f:
            return cls.from_md(filename, f.read())

    @classmethod
    def from_dict(cls, dct):
        parent = dct.get('parent')
        section = cls(
            parent=None,
            header=dct['header'],
            attributes=dct['attributes'],
            sections=[Section.from_dict(s) for s in dct['sections']],
            contents=[mdsplit.from_dict(o) for o in dct['contents']])

        for child in section.sections:
            child._parent = section

    def update_attributes(self, attributes):
        utils.update_dict(self.attributes, attributes)

    def append_section(self, section):
        assert section.level > 0
        if self.header is None or section.header.level < self.header.level:
            self.sections.append(section)
        else:
            self._parent.append_section(section)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other._tuple() == self._tuple()

    def _tuple(self):
        return (self.header, self.attributes, self.sections, self.contents)




# anchor_txt: attributes in markdown
#
# Copyright (C) 2019 Rett Berg <github.com/vitiral>
#
# The source code is Licensed under either of
#
# * Apache License, Version 2.0, ([LICENSE-APACHE](LICENSE-APACHE) or
#   http://www.apache.org/licenses/LICENSE-2.0)
# * MIT license ([LICENSE-MIT](LICENSE-MIT) or
#   http://opensource.org/licenses/MIT)
#
# at your option.
#
# Unless you explicitly state otherwise, any contribution intentionally submitted
# for inclusion in the work by you, as defined in the Apache-2.0 license, shall
# be dual licensed as above, without any additional terms or conditions.
"""
Section object
"""
from __future__ import unicode_literals
# Splits the file and pull out attributes and sections

import re
import six

import yaml

from . import utils
from . import mdsplit

ATTR_IDENTIFIER_RE = re.compile(r"^yaml .*@$")
ATTR_INLINE_RE = re.compile(r"`@{(.*?)}`")


class Section:
    """A section of markdown.

    This is either:
    - the entire markdown file (root section)
    - a section of markdown with a header at the top
    """

    TYPE = 'SECTION'

    #pylint: disable=too-many-arguments
    def __init__(self, parent, header, attributes, sections, contents):
        self.parent = parent
        self.header = header
        self.attributes = attributes
        self.sections = sections
        self.contents = contents

    def is_root(self):
        """Return whether this is the root/document Section."""
        return self.header is None

    @classmethod
    def from_md(cls, md_text):
        """Convert a markdown file to a Section."""
        components = mdsplit.split(md_text)
        root = _create_new_section(cls, None, None)
        current_section = root

        # Loop through the components, adding them to the correct section
        # and storing attributes.
        for cmt in components:
            if isinstance(cmt, mdsplit.Header):
                if current_section.is_root(
                ) or cmt.level < current_section.header.level:
                    parent = current_section
                else:
                    parent = current_section.parent

                new_section = _create_new_section(cls,
                                                  parent=parent,
                                                  header=cmt)
                _append_section(current_section, new_section)
                current_section = new_section
            elif isinstance(cmt, mdsplit.Code):
                if cmt.is_attributes:
                    code_txt = '\n'.join(cmt.text)
                    _update_attributes(current_section,
                                       yaml.safe_load(code_txt))
                current_section.contents.append(cmt)
            else:
                assert isinstance(cmt, mdsplit.Text)
                for line in cmt.raw:
                    for match in ATTR_INLINE_RE.finditer(line):
                        value = utils.to_unicode(yaml.safe_load(
                            match.group(1)))
                        if isinstance(value, six.text_type):
                            value = {value: None}
                        _update_attributes(current_section, value)

                current_section.contents.append(cmt)

        return root

    @classmethod
    def from_md_path(cls, path):
        """Convert a markdown file at a path to a Section."""
        with open(path) as fdesc:
            return cls.from_md(fdesc.read())

    def to_dict(self):
        """serialize."""
        return {
            "type": self.TYPE,
            "header": self.header.to_dict() if self.header else None,
            "attributes": self.attributes,
            "sections": [s.to_dict() for s in self.sections],
            "contents": [c.to_dict() for c in self.contents],
        }

    @classmethod
    def from_dict(cls, dct):
        """deserialize"""
        assert dct['type'] == cls.TYPE
        section = cls(parent=None,
                      header=dct['header'],
                      attributes=dct['attributes'],
                      sections=[Section.from_dict(s) for s in dct['sections']],
                      contents=[mdsplit.from_dict(o) for o in dct['contents']])

        for child in section.sections:
            child.parent = section

        return section

    #pylint: disable=protected-access
    def __eq__(self, other):
        return isinstance(other,
                          self.__class__) and other._tuple() == self._tuple()

    def __repr__(self):
        return "Section(header={}, sections={})".format(
            self.header, self.sections)

    def _tuple(self):
        return (self.header, self.attributes, self.sections, self.contents)


def _create_new_section(cls, parent, header):
    return cls(parent=parent,
               header=header,
               attributes={},
               sections=[],
               contents=[])


def _update_attributes(section, attributes):
    """Update the attributes on a section."""
    utils.update_dict(section.attributes, attributes)


def _append_section(last_section, section):
    """ Appends the section to the correct parent, based on the level.

    Called when digesting a list of sections.
    """

    assert section.header.level > 0
    if last_section.is_root(
    ) or section.header.level > last_section.header.level:
        last_section.sections.append(section)
    else:
        _append_section(last_section.parent, section)

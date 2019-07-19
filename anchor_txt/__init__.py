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
anchor_txt: markdown with attributes

Anchor adds the ability to embed attributes in markdown files so that external
tools can more easily link them to eachother and code, as well as perform
other operations.

Use ``anchor_txt.Section.from_md_path`` to load a markdown file.

The syntax used is in the README.md
"""
from __future__ import print_function

from .section import Section
from .mdsplit import Header
from .mdsplit import Code
from .mdsplit import Text


def main(argv):
    """Main function for cmdline."""
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description=
        'Process a markdown file into sections and attributes and print to stdout'
    )
    parser.add_argument('path', help='path to a markdown file')
    parser.add_argument('--format',
                        help='format to output to (json or yaml)',
                        default='json')
    args = parser.parse_args(argv)

    sys.stderr.write('args.path={}\n'.format(args.path))
    root = Section.from_md_path(args.path).to_dict()
    if args.format == 'json':
        import json
        print(json.dumps(root, indent=4))
    elif args.format == 'yaml':
        import yaml
        print(yaml.safe_dump(root, indent=4))
    else:
        sys.stderr.write('Invalid --format={}\n'.format(args.format))
        return 1
    return 0

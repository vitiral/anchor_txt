from __future__ import print_function

from .section import Section
from .mdsplit import Header
from .mdsplit import Code
from .mdsplit import Text


def main(argv):
    import sys
    import argparse
    import yaml

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

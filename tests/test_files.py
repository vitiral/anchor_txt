"""
This uses the data in tests/files
- The *.md files contain what should be parsed.
- The *.json files contain what is expected.
"""

import os
import json
import unittest
from anchor import mdsplit

SCRIPT_PATH = os.path.realpath(__file__)
TEST_DIR = os.path.dirname(SCRIPT_PATH)
FILES_DIR = os.path.join(TEST_DIR, "files")


def read(path):
    with open(path) as f:
        return f.read()

def read_json(path):
    with open(path) as f:
        j = json.load(f)

    return [mdsplit.from_dict(o) for o in j]


def file_test(name):
    expected = read_json(os.path.join(FILES_DIR, name + '.json'))
    md = read(os.path.join(FILES_DIR, name + '.md'))
    assert expected == mdsplit.split(md), "for file " + name


class TestFiles(unittest.TestCase):
    def test_word(self):
        file_test('word')

    def test_header(self):
        file_test('header')

    def test_anchor(self):
        file_test('anchor')

    def test_header_multi(self):
        file_test('header_multi')

    def test_code_fence(self):
        file_test('code-fence')

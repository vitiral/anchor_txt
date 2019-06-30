
import os
import json
import unittest
from anchor import mdsplit
from anchor import attributes

SCRIPT_PATH = os.path.realpath(__file__)
TEST_DIR = os.path.dirname(SCRIPT_PATH)
SPLITS_DIR = os.path.join(TEST_DIR, "splits")
ATTRS_DIR = os.path.join(TEST_DIR, "attributes")


def read(path):
    with open(path) as f:
        return f.read()

def read_json(path):
    with open(path) as f:
        return json.load(f)


def split_test(name):
    expected = read_json(os.path.join(SPLITS_DIR, name + '.json'))
    md = read(os.path.join(SPLITS_DIR, name + '.md'))
    result = [c.to_dict() for c in mdsplit.split(md)]
    assert expected == result, "for file " + name


def attr_test(name):
    expected = read_json(os.path.join(ATTRS_DIR, name + '.json'))
    md_path = os.path.join(ATTRS_DIR, name + '.md')
    result = attributes.Section.from_md_path(md_path).to_dict()
    assert expected == result, "for file " + name


class TestSplit(unittest.TestCase):
    """
    This uses the data in tests/splits
    - The *.md files contain what should be parsed.
    - The *.json files contain what is expected.
    """
    def test_word(self):
        split_test('word')

    def test_header(self):
        split_test('header')

    def test_anchor(self):
        split_test('anchor')

    def test_header_multi(self):
        split_test('header_multi')

    def test_code_fence(self):
        split_test('code-fence')


class TestAttributes(unittest.TestCase):
    def test_word(self):
        attr_test('word')

    def test_header(self):
        attr_test('header')

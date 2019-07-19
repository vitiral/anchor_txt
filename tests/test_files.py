
import os
import json
import unittest
from anchor import mdsplit
from anchor import section

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


class TestSplit(unittest.TestCase):
    """
    This uses the data in tests/splits
    - The *.md files contain what should be parsed.
    - The *.json files contain what is expected.
    """

    def run_file(self, name):
        expected = read_json(os.path.join(SPLITS_DIR, name + '.json'))
        md = read(os.path.join(SPLITS_DIR, name + '.md'))
        result = [c.to_dict() for c in mdsplit.split(md)]
        assert expected == result, "for file " + name

    def test_word(self):
        self.run_file('word')

    def test_header(self):
        self.run_file('header')

    def test_anchor(self):
        self.run_file('anchor')

    def test_header_multi(self):
        self.run_file('header_multi')

    def test_code_fence(self):
        self.run_file('code-fence')


class TestAttributes(unittest.TestCase):
    def run_file(self, name):
        expected = read_json(os.path.join(ATTRS_DIR, name + '.json'))
        md_path = os.path.join(ATTRS_DIR, name + '.md')
        result = section.Section.from_md_path(md_path).to_dict()
        assert expected == result, "for file " + name

    def test_word(self):
        self.run_file('word')

    def test_header(self):
        self.run_file('header')

    def test_header_multi(self):
        self.run_file('sub-header')

    def test_code_fence(self):
        self.run_file('code-fence')

    def test_code_attributes(self):
        self.run_file('code-attributes')

    def test_text_attributes(self):
        self.run_file('text-attributes')

import os
import json
import unittest
import anchor_txt

SCRIPT_PATH = os.path.realpath(__file__)
TEST_DIR = os.path.dirname(SCRIPT_PATH)
SPLITS_DIR = os.path.join(TEST_DIR, "splits")
ATTRS_DIR = os.path.join(TEST_DIR, "attributes")


def read(path):
    with open(path) as f:
        return f.read()


def read_lines(path):
    return anchor_txt.utils.to_unicode(read(path)).split('\n')


def read_json(path):
    with open(path) as f:
        return json.load(f)


class TestSplit(unittest.TestCase):
    """
    This uses the data in tests/splits
    - The *.md files contain what should be parsed.
    - The *.json files contain what is expected.
    """
    def run_test(self, name):
        expected = read_json(os.path.join(SPLITS_DIR, name + '.json'))
        md = read(os.path.join(SPLITS_DIR, name + '.md'))
        result = [c.to_dict() for c in anchor_txt.mdsplit.split(md)]
        assert expected == result, "for file " + name

    def test_word(self):
        self.run_test('word')

    def test_header(self):
        self.run_test('header')

    def test_anchor(self):
        self.run_test('anchor')

    def test_header_multi(self):
        self.run_test('header_multi')

    def test_code_fence(self):
        self.run_test('code-fence')

    def test_reference_links(self):
        self.run_test('reference-links')

    def test_reference_links(self):
        self.run_test('anchor_html')


class TestAttributes(unittest.TestCase):
    def run_test(self, name):
        expected = read_json(os.path.join(ATTRS_DIR, name + '.json'))
        md_path = os.path.join(ATTRS_DIR, name + '.md')
        section = anchor_txt.section.Section.from_md_path(md_path)
        result = section.to_dict()
        assert expected == result, "section for file " + name

        result = section.to_lines()
        expected = read_lines(md_path)
        assert expected == result, "lines for file " + name

    def test_word(self):
        self.run_test('word')

    def test_header(self):
        self.run_test('header')

    def test_header_multi(self):
        self.run_test('sub-header')

    def test_code_fence(self):
        self.run_test('code-fence')

    def test_code_attributes(self):
        self.run_test('code-attributes')

    def test_code_attributes(self):
        self.run_test('code-attributes-json')

    def test_text_attributes(self):
        self.run_test('text-attributes')

    def test_reference_links(self):
        self.run_test('reference-links')

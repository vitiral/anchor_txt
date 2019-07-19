"""
There are several util functions which should be tested
"""

import os
import copy
import json
import unittest
from anchor import utils


class TestUtils(unittest.TestCase):
    def test_update_empty(self):
        a = {'a': 2}
        expect = copy.deepcopy(a)
        utils.update_dict(a, {})
        assert expect == a

    def test_update_simple(self):
        a = {'a': 2}
        b = {'b': 3}
        expect = {'a': 2, 'b': 3}
        utils.update_dict(a, b)
        assert expect == a

    def test_update_override(self):
        a = {'a': 1}
        a2 = {'a': 2}

        try:
            utils.update_dict(a, a2)
            assert False
        except ValueError:
            pass

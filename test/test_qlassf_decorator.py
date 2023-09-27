import unittest

from qlasskit import QlassF, qlassf

from . import utils


class TestQlassfDecorator(unittest.TestCase):
    def test_decorator(self):
        c = qlassf(utils.test_not)
        self.assertTrue(isinstance(c, QlassF))

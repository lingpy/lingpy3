from __future__ import unicode_literals
from unittest import TestCase

from lingpy3 import util


class Tests(TestCase):
    def test_combinations2(self):
        def f(l):
            for i, a1 in enumerate(l):
                for j, a2 in enumerate(l):
                    if i < j:
                        yield a1, a2

        def fm(l):
            for i, a1 in enumerate(l):
                for j, a2 in enumerate(l):
                    if i <= j:
                        yield a1, a2

        for l in [list(range(5)), 'abcdefg']:
            self.assertEqual(list(util.combinations2(l)), list(f(l)))
            self.assertEqual(list(util.multicombinations2(l)), list(fm(l)))

    def test_identity(self):
        for thing in [None, 'x', 3]:
            self.assertEqual(util.identity(thing), thing)

    def test_setdefaults(self):
        d = {'a': 1}
        util.setdefaults(d, a=3, b=1)
        self.assertEqual(d['a'], 1)
        self.assertEqual(d['b'], 1)

    def test_charstring(self):
        self.assertEqual(util.charstring('abc'), 'abc.X.-')

    def test_join(self):
        self.assertEqual(util.join('.'), '')
        self.assertEqual(util.join('.', 1), '1')
        self.assertEqual(util.join('.', 1, 2), '1.2')

    def test_dotjoin(self):
        self.assertEqual(util.dotjoin(1, 2), '1.2')
        self.assertEqual(util.dotjoin([1, 2]), '1.2')
        self.assertEqual(util.dotjoin((1, 2)), '1.2')
        self.assertEqual(
            util.dotjoin((i for i in range(1, 3)), condition=lambda j: j > 1), '2')
        self.assertEqual(util.dotjoin(i for i in range(1, 3)), '1.2')

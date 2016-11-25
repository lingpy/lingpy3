# coding: utf8
from __future__ import unicode_literals, print_function, division
from unittest import TestCase

from lingpy3.tests.fixtures import make_wordlist


class Tests(TestCase):
    def test_misc(self):
        from lingpy3.ops import run, list_ops_doc

        wl = make_wordlist()
        self.assertIn('distances', set(spec[0] for spec in list_ops_doc(wl)))
        self.assertIsInstance(run('distances', wl), list)

# coding: utf8
from __future__ import unicode_literals, print_function, division
from unittest import TestCase


class Tests(TestCase):
    def test_Settings(self):
        from lingpy3.settings import LexstatSettings

        s = LexstatSettings()
        self.assertEqual(s.asdict()['runs'], 1000)

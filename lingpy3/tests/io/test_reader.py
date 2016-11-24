# coding: utf8
from __future__ import unicode_literals, print_function, division
from unittest import TestCase

from clldutils.path import Path


class Tests(TestCase):
    def test_wrapping(self):
        from lingpy3.io.reader.base import wrapped, unwrapped

        for obj in [2, 'a', Path('.')]:
            self.assertEqual(obj, unwrapped(wrapped(obj)))

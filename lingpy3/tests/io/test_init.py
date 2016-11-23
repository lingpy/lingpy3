# coding: utf8
from __future__ import unicode_literals, print_function, division

from clldutils.testing import WithTempDir


class Tests(WithTempDir):
    def test_create_representation(self):
        from lingpy3.basic.wordlist import Wordlist
        from lingpy3.io import write, read

        wl = Wordlist(['id', 'concept', 'doculect'], [['ä', 'ö', 'ü']])
        out = write(wl, 'csv', self.tmp_path(), 'test', delimiter='\t')
        self.assertTrue(out.exists())
        wl2 = read(out, Wordlist, 'csv', delimiter='\t')
        self.assertEqual(wl[1], wl2[1])

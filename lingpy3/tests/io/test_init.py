# coding: utf8
from __future__ import unicode_literals, print_function, division

from clldutils.testing import WithTempDir

from lingpy3.interfaces import IWordlist
from lingpy3.basic.wordlist import Wordlist


class Tests(WithTempDir):
    def test_misc(self):
        from lingpy3.io import write, read, iter_writers, get, iter_readers

        self.assertTrue(bool(list(iter_readers(self.tmp_path(), IWordlist))))
        wl = Wordlist(['id', 'concept', 'doculect', 'cogid'], [['ä', 'ö', 'ü', '1']])
        out = write(wl, 'csv', self.tmp_path(), 'test', delimiter='\t')
        self.assertTrue(out.exists())
        wl2 = read(out, IWordlist, 'csv', delimiter='\t')
        self.assertEqual(wl[1], wl2[1])
        with out.open(encoding='utf8') as fp:
            wl3 = read(fp.read(), Wordlist, 'csv', delimiter='\t')
            self.assertEqual(wl[1], wl3[1])

        for name, _ in iter_writers(wl):
            get(wl, name)

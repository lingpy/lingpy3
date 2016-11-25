# coding: utf8
from __future__ import unicode_literals, print_function, division

from clldutils.testing import WithTempDir

from lingpy3.interfaces import IWordlist, ISoundClassModel
from lingpy3.basic.wordlist import Wordlist
from lingpy3 import registry
from lingpy3.tests.fixtures import make_wordlist


class Tests(WithTempDir):
    def test_misc(self):
        from lingpy3.io import write, read, list_writers_doc, get, list_readers_doc

        self.assertTrue(bool(list_readers_doc(IWordlist, self.tmp_path())))
        wl = make_wordlist()
        out = write('csv', wl, _outdir=self.tmp_path(), _stem='test', delimiter='\t')
        self.assertTrue(out.exists())
        wl2 = read('csv', Wordlist, out, delimiter='\t')
        self.assertEqual(wl[1], wl2[1])
        with out.open(encoding='utf8') as fp:
            wl3 = read('csv', IWordlist, fp.read(), delimiter='\t')
            self.assertEqual(wl[1], wl3[1])

        for name, _, mod in list_writers_doc(wl):
            get(name, wl)

        scm = registry.get(ISoundClassModel, 'asjp')
        self.assertIn('Brown', get('txt', scm))

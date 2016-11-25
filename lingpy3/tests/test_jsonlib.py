# coding: utf8
from __future__ import unicode_literals, print_function, division
from collections import OrderedDict

from clldutils.testing import WithTempDir

from lingpy3.basic.wordlist import Wordlist
from lingpy3.tests.fixtures import make_wordlist


class Tests(WithTempDir):
    def test_dump_load_dict(self):
        from lingpy3.jsonlib import load, dump

        d = {'a': 2, 'z': 1}
        out = dump(d, outdir=self.tmp_path())
        self.assertEqual(d, load(out))
        d2 = OrderedDict([('z', 1), ('a', 2)])
        out2 = dump(d2, outdir=self.tmp_path())
        self.assertEqual(out.name, out2.name)

    def test_dump_load_custom(self):
        from lingpy3.jsonlib import load, dump

        wl = make_wordlist()
        out = dump(wl, outdir=self.tmp_path())
        self.assertEqual(wl, load(out, Wordlist))

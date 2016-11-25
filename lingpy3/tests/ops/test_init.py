# coding: utf8
from __future__ import unicode_literals, print_function, division

from clldutils.testing import WithTempDir
from mock import patch

from lingpy3.tests.fixtures import make_wordlist


class Tests(WithTempDir):
    def test_misc(self):
        from lingpy3.ops import run, list_ops_doc

        wl = make_wordlist()
        self.assertIn('distances', set(spec[0] for spec in list_ops_doc(wl)))
        self.assertIsInstance(run('distances', wl), list)

    def test_run_and_dump(self):
        from lingpy3.ops import run_and_dump
        from lingpy3.jsonlib import path_from_checksum

        with patch('lingpy3.ops.CACHE_DIR', self.tmp_path()):
            wl = make_wordlist()
            res, checksum = run_and_dump('distances', wl)
            run_and_dump('distances', wl, __checksum__=checksum)
            self.assertTrue(path_from_checksum(checksum, outdir=self.tmp_path()).exists())

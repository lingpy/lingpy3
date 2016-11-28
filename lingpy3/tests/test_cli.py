# coding: utf8
from __future__ import unicode_literals, print_function, division

from clldutils.testing import WithTempDir, capture

from lingpy3 import cli
from lingpy3.tests.fixtures import make_wordlist
from lingpy3.io import write


class Tests(WithTempDir):
    def test_help(self):
        with capture(cli.main, 'help', 'operation') as out:
            self.assertIn('positional arguments', out)

    def test_operation(self):
        wl = write('csv', make_wordlist(), _outdir=self.tmp_path(), delimiter=',')
        args = '-o {0} operation distances csv:IWordlist:{1}:delimiter=,'.format(
            self.tmp_path(), wl)
        with capture(cli.main, *args.split()) as out:
            self.assertIn('written', out)
        self.assertTrue(bool(list(self.tmp_path().glob('*.json'))))

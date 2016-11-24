# coding: utf8
from __future__ import unicode_literals, print_function, division

from six import PY2, BytesIO, StringIO
from zope.interface import implementer
from zope.component import adapts
from clldutils.dsv import reader

from lingpy3.interfaces import IWordlist, IPath, IText
from lingpy3.basic.wordlist import Wordlist
from lingpy3.io.reader.base import BaseReader


@implementer(IWordlist)
class CsvBase(BaseReader):
    name = 'csv'

    def _get_input(self):
        return self.obj

    def __call__(self, **kw):
        rows = list(reader(self._get_input(), delimiter=kw.pop('delimiter', None)))
        return Wordlist(rows[0], rows[1:], **kw)


class Csv(CsvBase):
    adapts(IPath)


class CsvFromText(Csv):
    adapts(IText)

    def _get_input(self):
        f = BytesIO(self.obj.encode('utf8')) if PY2 else StringIO(self.obj)
        f.seek(0)
        return f

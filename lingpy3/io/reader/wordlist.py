# coding: utf8
from __future__ import unicode_literals, print_function, division

from zope.interface import implementer
from zope.component import adapts
from clldutils.dsv import reader

from lingpy3.interfaces import IWordlist, IPath
from lingpy3.basic.wordlist import Wordlist
from lingpy3.io.reader.base import BaseReader


@implementer(IWordlist)
class Csv(BaseReader):
    name = 'csv'
    adapts(IPath)

    def __call__(self, **kw):
        rows = list(reader(self.obj, delimiter=kw.pop('delimiter', None)))
        return Wordlist(rows[0], rows[1:], **kw)

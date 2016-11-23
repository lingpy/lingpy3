# coding: utf8
from __future__ import unicode_literals, print_function, division

from zope.interface import implementer
from zope.component import adapts

from lingpy3.interfaces import IWriter, IWordlist, ISoundClassModel


@implementer(IWriter)
class BaseWriter(object):
    def __init__(self, obj):
        self.obj = obj

    def get(self, **kw):  # pragma: no cover
        raise NotImplemented()

    def write(self, path, **kw):
        with path.open('w', encoding='utf8') as fp:
            fp.write(self.get(**kw))


class Txt(BaseWriter):
    name = 'txt'
    adapts(IWordlist, ISoundClassModel)

    def get(self, **kw):
        return '%s' % self.obj

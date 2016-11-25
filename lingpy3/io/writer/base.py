# coding: utf8
from __future__ import unicode_literals, print_function, division

from zope.interface import implementer

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


def writer(adapts, name=None):
    """
    Decorator for simplified implementation and registration of IWriters.

    :param adapts: The interface which is adapted to IWriter.
    :param name: The name under which to register the IWriter - defaults to the name of \
    the decorated function (with "_" replaced by ".").
    :return: The (unchanged) decorated function.
    """
    def wrap(f):
        from lingpy3.registry import register_adapter_from_factory
        register_adapter_from_factory(
            f,
            adapts,
            BaseWriter,
            clsname='Writer_{0}_{1}'.format(adapts.__name__, name or f.__name__),
            get=lambda self, **kw: f(self.obj, **kw),
            name=name or f.__name__.replace('_', '.'))
        return f
    return wrap


@writer(IWordlist)
@writer(ISoundClassModel)
def txt(obj, **kw):
    return '%s' % obj

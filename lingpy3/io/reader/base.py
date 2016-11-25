# coding: utf8
"""

"""
from __future__ import unicode_literals, print_function, division

from zope.interface import implementer
from six import text_type
from clldutils.path import Path

from lingpy3 import interfaces


# To make the ZCA adapter mechanisms work for reader classes, we must make text and path
# types available for adaption. Since these types are defined outside of lingpy3, we just
# provide wrappers, implementing the corresponding interfaces.
class Wrapper(object):
    def __init__(self, obj):
        self.obj = obj


@implementer(interfaces.IText)
class TextWrapper(Wrapper):
    pass


@implementer(interfaces.IPath)
class PathWrapper(Wrapper):
    pass


def wrapped(obj):
    if isinstance(obj, text_type):
        return TextWrapper(obj)
    if isinstance(obj, Path):
        return PathWrapper(obj)
    return obj


def unwrapped(obj):
    if isinstance(obj, Wrapper):
        return obj.obj
    return obj


class BaseReader(object):
    """
    Virtual base class for Reader objects.

    Derived classes must declare the interface of the object they return when called
    using the @implementer decorator.
    """
    name = ''

    def __init__(self, obj):
        self.obj = unwrapped(obj)

    def __call__(self, **kw):
        """
        When called, a Reader must return an initialized object providing the interface.
        """
        raise NotImplemented()  # pragma: no cover


def reader(adapts, provides, name=None):
    """
    Decorator for simplified implementation and registration of readers.

    :param provides: The interface to which an input object is adapter.
    :param name: The name under which to register the IWriter - defaults to the name of \
    the decorated function (with "_" replaced by ".").
    :return: The (unchanged) decorated function.
    """
    def wrap(f):
        from lingpy3.registry import register_adapter_from_factory
        register_adapter_from_factory(
            f,
            adapts,
            BaseReader,
            provides=provides,
            clsname='Writer_{0}_{1}'.format(provides.__name__, name or f.__name__),
            __call__=lambda self, **kw: f(self.obj, **kw),
            name=name or f.__name__.replace('_', '.'))
        return f
    return wrap

# coding: utf8
from __future__ import unicode_literals, print_function, division

from zope.interface import implementer

from lingpy3 import interfaces


@implementer(interfaces.IOperation)
class BaseOperation(object):
    """
    Virtual base class for Operation objects.
    """
    def __init__(self, obj):
        self.obj = obj

    def __call__(self, **kw):
        """
        When called, a Reader must return an initialized object providing the interface.
        """
        raise NotImplemented()  # pragma: no cover


def operation(adapts, name=None):
    """
    Decorator for simplified implementation and registration of IOperations.
    """
    def wrap(f):
        from lingpy3.registry import register_adapter_from_factory
        register_adapter_from_factory(
            f,
            adapts,
            BaseOperation,
            clsname='Operation_{0}_{1}'.format(adapts.__name__, name or f.__name__),
            __call__=lambda self, **kw: f(self.obj, **kw),
            name=name or f.__name__)
        return f
    return wrap

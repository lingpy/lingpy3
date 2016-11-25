# coding: utf8
from __future__ import unicode_literals, print_function, division

from six import binary_type, PY2
from zope.interface import providedBy, implementedBy
from zope.interface.registry import Components
from zope.interface.verify import verifyObject
from zope.component import adaptedBy


_registry = None
ADAPTER_COUNT = 0


def get_registry():
    global _registry
    if _registry is None:
        _registry = Components()
    return _registry


def register_adapter_from_factory(f, adapts, base, provides=None, clsname='A', **clsdict):
    global ADAPTER_COUNT
    ADAPTER_COUNT += 1
    clsdict.setdefault('__doc__', f.__doc__ or '')
    clsdict.setdefault('__source__', '%s.%s' % (f.__module__, f.__name__))
    clsname = '%s_%s' % (clsname, ADAPTER_COUNT)
    register_adapter(
        type(binary_type(clsname) if PY2 else clsname, (base,), clsdict),
        from_=adapts,
        to_=provides)


def get_interface(thing):
    res = list(providedBy(thing))
    if len(res) == 1:
        return res[0]
    res = list(implementedBy(thing))
    if len(res) == 1:
        return res[0]
    return thing


def register_adapter(cls, from_=None, to_=None, name=None):
    from_ = from_ or adaptedBy(cls)
    if not isinstance(from_, (list, tuple)):
        from_ = (from_,)
    reg = get_registry()
    reg.registerAdapter(
        cls,
        required=from_,
        provided=to_ or get_interface(cls),
        name=name or getattr(cls, 'name', ''))


def get_adapter(obj, interface, name=None):
    reg = get_registry()
    return reg.getAdapter(obj, interface, name=name or '')


def get_adapters(obj, interface):
    reg = get_registry()
    return reg.getAdapters((obj,), interface)


def format_adapters_doc(adapters):
    return [(name, a.__doc__ or '', getattr(a, '__source__', None) or a.__module__)
            for name, a in adapters]


def register(obj, interface=None, name=None, verify=True):
    interface = interface or get_interface(obj)
    if verify:
        verifyObject(interface, obj)
    reg = get_registry()
    reg.registerUtility(obj, interface, name or getattr(obj, 'name', ''))


def get(interface, name=None):
    reg = get_registry()
    return reg.getUtility(interface, name or '')

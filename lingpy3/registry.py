# coding: utf8
from __future__ import unicode_literals, print_function, division
import inspect

from zope.interface import providedBy, implementedBy, Interface
from zope.interface.registry import Components
from zope.interface.verify import verifyObject
from zope.component import adaptedBy


_registry = None


def get_registry():
    global _registry
    if _registry is None:
        _registry = Components()
    return _registry


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


def register(obj, interface=None, name=None, verify=True):
    interface = interface or get_interface(obj)
    if verify:
        verifyObject(interface, obj)
    reg = get_registry()
    reg.registerUtility(obj, interface, name or getattr(obj, 'name', ''))


def get(interface, name=None):
    reg = get_registry()
    return reg.getUtility(interface, name or '')

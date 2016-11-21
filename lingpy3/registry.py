# coding: utf8
from __future__ import unicode_literals, print_function, division

from zope.interface import providedBy
from zope.interface.registry import Components
from zope.interface.verify import verifyObject


_registry = None


def get_registry():
    global _registry
    if _registry is None:
        _registry = Components()
    return _registry


def register(obj, interface=None, name=None, verify=True):
    interface = interface or list(providedBy(obj))[0]
    if verify:
        verifyObject(interface, obj)
    reg = get_registry()
    reg.registerUtility(
        obj,
        interface or list(providedBy(obj))[0],
        name or getattr(obj, 'name', ''))


def get(interface, name=None):
    reg = get_registry()
    return reg.getUtility(interface, name or '')

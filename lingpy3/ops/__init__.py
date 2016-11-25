# coding: utf8
from __future__ import unicode_literals, print_function, division

# Note: We have to import all modules which register adapters to make sure these adapter
# are already registered before a user can override these by re-registering.
from lingpy3 import interfaces
from lingpy3.registry import get_adapter, get_adapters, format_adapters_doc
from lingpy3.ops import wordlist


def run(name, obj, **kw):
    adapter = get_adapter(obj, interfaces.IOperation, name=name)
    return adapter(**kw)


def iter_ops(obj):
    return get_adapters(obj, interfaces.IOperation)


def list_ops_doc(obj):
    return format_adapters_doc(iter_ops(obj))

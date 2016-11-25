# coding: utf8
from __future__ import unicode_literals, print_function, division

from clldutils.path import as_unicode

# Note: We have to import all modules which register adapters to make sure these adapter
# are already registered before a user can override these by re-registering.
from lingpy3 import interfaces
from lingpy3.registry import get_adapter, get_adapters, format_adapters_doc
from lingpy3.ops import wordlist
from lingpy3.jsonlib import load, dump, path_from_checksum
from lingpy3.cache import CACHE_DIR


def run(name, obj, **kw):
    adapter = get_adapter(obj, interfaces.IOperation, name=name)
    return adapter(**kw)


def run_and_dump(name, obj, __checksum__=None, **kw):
    adapter = get_adapter(obj, interfaces.IOperation, name=name)
    if __checksum__:
        cached = path_from_checksum(__checksum__, outdir=CACHE_DIR)
        if cached.exists():
            return load(cached, cls=adapter.returns), __checksum__
    res = adapter(**kw)
    out = dump(res, outdir=CACHE_DIR)
    return res, as_unicode(out.stem)


def iter_ops(obj):
    return get_adapters(obj, interfaces.IOperation)


def list_ops_doc(obj):
    return format_adapters_doc(iter_ops(obj))

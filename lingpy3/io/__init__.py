# coding: utf8
"""
LingPy3 input and output functionality

Input means creating lingpy3 objects from user input such as text or files. Generally,
this is realized through readers (adapters in ZCA lingo), adapting the type of user input
to the desired lingpy3 interface.

Output means converting lingpy3 objects to text or files. This is implemented via writers,
again adapters, this time from a lingpy3 object interface to IWriter.

Since both, readers and writers are adapters, it is easy
- to add more (by providing additional implementations and adding these to the registry)
- to customize existing readers or writers, by registering customizations under the same
  same name.
"""
from __future__ import unicode_literals, print_function, division

from clldutils.path import path_component

# Note: We have to import all modules which register adapters to make sure these adapter
# are already registered before a user can override these by re-registering.
from lingpy3.log import file_written
from lingpy3.registry import get_adapter, get_interface, get_adapters, format_adapters_doc
from lingpy3 import interfaces
from lingpy3.io.reader import base as readbase
from lingpy3.io.reader import wordlist as readwl
from lingpy3.io.writer import base
from lingpy3.io.writer import wordlist


def read(name, interface, obj, **kw):
    adapter = get_adapter(readbase.wrapped(obj), get_interface(interface), name=name)
    return adapter(**kw)


def get(name, obj, **kw):
    adapter = get_adapter(obj, interfaces.IWriter, name=name)
    return adapter.get(**kw)


def write(name, obj, _outdir=None, _stem=None, **kw):
    adapter = get_adapter(obj, interfaces.IWriter, name=name)
    outfile = _outdir.joinpath(path_component('{0}.{1}'.format(_stem, name)))
    adapter.write(outfile, **kw)
    file_written(outfile)
    return outfile


def iter_writers(obj):
    return get_adapters(obj, interfaces.IWriter)


def list_writers_doc(obj):
    return format_adapters_doc(iter_writers(obj))


def iter_readers(interface, obj):
    return get_adapters(readbase.wrapped(obj), get_interface(interface))


def list_readers_doc(interface, obj):
    return format_adapters_doc(iter_readers(interface, obj))

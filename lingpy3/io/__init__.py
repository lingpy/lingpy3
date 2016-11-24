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

from lingpy3.log import file_written
from lingpy3.registry import get_adapter, register_adapter, get_interface, get_adapters
from lingpy3 import interfaces
from lingpy3.io.reader import base as readbase
from lingpy3.io.reader import wordlist as readwl
from lingpy3.io.writer import base as writebase
from lingpy3.io.writer import wordlist as writewl

for adapter in [
    (writebase.Txt, interfaces.IWordlist),
    (writebase.Txt, interfaces.ISoundClassModel),
    (writewl.Csv,),
    (writewl.PapsNex,),
    (readwl.Csv,),
    (readwl.CsvFromText,),
]:
    register_adapter(*adapter)


def read(obj, interface, name, **kw):
    adapter = get_adapter(readbase.wrapped(obj), get_interface(interface), name=name)
    return adapter(**kw)


def get(obj, name, **kw):
    adapter = get_adapter(obj, interfaces.IWriter, name=name)
    return adapter.get(**kw)


def write(obj, name, outdir=None, stem=None, **kw):
    adapter = get_adapter(obj, interfaces.IWriter, name=name)
    outfile = outdir.joinpath(path_component('{0}.{1}'.format(stem, name)))
    adapter.write(outfile, **kw)
    file_written(outfile)
    return outfile


def iter_writers(obj):
    return get_adapters(obj, interfaces.IWriter)


def iter_readers(obj, interface):
    return get_adapters(readbase.wrapped(obj), get_interface(interface))

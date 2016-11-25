# coding: utf8
from __future__ import unicode_literals, print_function, division
from hashlib import md5
import json

from six import text_type
from clldutils.path import Path, path_component
from clldutils.jsonlib import load as cu_load


def dump(obj, outdir=None, stem=None):
    if hasattr(obj, '__json__'):
        obj = obj.__json__()
    val = json.dumps(obj, indent=4, sort_keys=True)
    if isinstance(val, text_type):
        val = val.encode('utf8')  # pragma: no cover
    outfile = path_from_checksum(stem or md5(val).hexdigest(), outdir=outdir)
    with outfile.open('wb') as fp:
        fp.write(val)
    return outfile


def path_from_checksum(checksum, outdir=None):
    return (outdir or Path('.')).joinpath(path_component('{0}.json'.format(checksum)))


def load(path, cls=None):
    val = cu_load(path)
    if cls:
        val = cls.__from_json__(val)
    return val

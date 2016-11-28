# coding: utf8
from __future__ import unicode_literals, print_function, division

from six import PY2, BytesIO, StringIO
from clldutils import dsv

from lingpy3.interfaces import IWordlist, IPath, IText
from lingpy3.basic.wordlist import Wordlist
from lingpy3.io.reader.base import reader


def _read_csv(obj, **kw):
    rows = list(dsv.reader(obj, delimiter=kw.pop('delimiter', '\t')))
    return Wordlist(rows[0], rows[1:], **kw)


@reader(IPath, IWordlist)
def csv(path, **kw):
    """
    Read a CSV (or TSV) file into a Wordlist object.

    :param path:
    :param kw:
    :return:
    """
    return _read_csv(path, **kw)


@reader(IText, IWordlist, name='csv')
def csv_from_text(text, **kw):
    f = BytesIO(text.encode('utf8')) if PY2 else StringIO(text)
    f.seek(0)
    return _read_csv(f, **kw)

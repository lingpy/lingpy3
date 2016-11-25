from __future__ import division, unicode_literals
from functools import partial
import itertools
import types
import unicodedata

from tqdm import tqdm
from clldutils.path import Path
from clldutils import clilib

import lingpy3


# Shortcut to create a progress bar which will disappear after completion:
pb = partial(tqdm, leave=False)


def read_text(path, normalize=None):
    """
    Read a text file encoded in utf-8.

    Parameters
    ----------
    path : { Path, str }
        File-system path of the file.
    normalize : { None, "NFC", "NFC" }
        If not `None` a valid unicode normalization mode must be passed.

    Returns
    -------
    file_content : { str }
        File content as unicode object.

    Notes
    -----
    The whole file is read into memory.

    """
    with path.open('r', encoding='utf8') as fp:
        res = fp.read()
    if normalize:
        res = unicodedata.normalize(normalize, res)
    return res


def read_lines(path, normalize=None):
    with path.open('r', encoding='utf8') as fp:
        res = [line.strip('\r\n') for line in fp]
    if normalize:
        res = [unicodedata.normalize(normalize, line) for line in res]
    return res


def uniq(iterable):
    return sorted(set(iterable))


def charstring(id_, char='X', cls='-'):
    return '{0}.{1}.{2}'.format(id_, char, cls)


def combinations2(iterable):
    """
    Convenience shortcut
    """
    return itertools.combinations(iterable, 2)


def multicombinations2(iterable):
    """
    Convenience shortcut, for the name, see the Wikipedia article on Combination.

    https://en.wikipedia.org/wiki/Combination#Number_of_combinations_with_repetition
    """
    return itertools.combinations_with_replacement(iterable, 2)


product2 = partial(itertools.product, repeat=2)


def chained_values(d):
    """
    Concatenate the values of a `list`-valued `dict`.

    :param d:
    :return: `list`
    """
    return list(itertools.chain(*d.values()))


def join(sep, *args, **kw):
    """
    Convenience shortcut. Strings to be joined do not have to be passed as list or tuple.

    Notes
    -----
    An implicit conversion of objects to strings is performed as well.

    """
    if len(args) == 1 and isinstance(args[0], (list, tuple, types.GeneratorType)):
        args = args[0]
    condition = kw.get('condition', lambda x: True)
    return sep.join(['%s' % arg for arg in args if condition(arg)])


dotjoin = partial(join, '.')
tabjoin = partial(join, '\t')
confirm = partial(clilib.confirm, default=False)


def pkg_path(*comps):
    return Path(lingpy3.__file__).parent.joinpath(*comps)


data_path = partial(pkg_path, 'data')


def setdefaults(d, **kw):
    """Shortcut for a common idiom, setting multiple default values at once.

    Parameters
    ----------
    d : dict
        Dictionary to be updated.
    kw : dict
        Dictionary with default values.
    """
    for k, v in kw.items():
        d.setdefault(k, v)


def identity(x):
    return x

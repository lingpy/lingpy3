# coding: utf8
from __future__ import unicode_literals, print_function, division
import re

from zope.interface import implementer
from clldutils.misc import UnicodeMixin
from clldutils.path import as_unicode
from clldutils.dsv import reader

from lingpy3.interfaces import ISoundClassModel, IDiactriticsVowelsTones
from lingpy3.util import read_lines, uniq, data_path, read_text
from lingpy3.cache import Cache
from lingpy3 import log
from lingpy3.algorithm import ScoreDict
from lingpy3.sequence.scoretree import ScoreTree


class NamedObject(UnicodeMixin):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<{0} {1}>'.format(self.__class__.__name__, self.name)

    @classmethod
    def from_name(cls, name):
        return cls.from_path(data_path('models', name))

    @classmethod
    def from_path(cls, path):
        raise NotImplemented()  # pragma: no cover


@implementer(IDiactriticsVowelsTones)
class DiacriticsVowelsTones(NamedObject):
    def __init__(self, name, diacritics, vowels, tones):
        NamedObject.__init__(self, name)
        self.diacritics = diacritics
        self.vowels = vowels
        self.tones = tones

    def __eq__(self, other):
        return all(getattr(self, k) == getattr(other, k)
                   for k in 'diacritics vowels tones'.split())

    def __json__(self):
        return {k: getattr(self, k) for k in 'name diacritics vowels tones'.split()}

    @classmethod
    def __from_json__(cls, val):
        return cls(*[val[k] for k in 'name diacritics vowels tones'.split()])

    @classmethod
    def from_path(cls, path):
        cache = Cache()
        cache_key = 'DiacriticsVowelsTones.{0}'.format(as_unicode(path.name))
        if cache_key not in cache:
            cache[cache_key] = read_dvt(path)
        return cls(as_unicode(path.name), *cache[cache_key])


def read_dvt(path):
    def _read_string(name):
        # TODO: this is potentially dangerous and it is important to decide whether
        # switching to NFD might not be a better choice
        return read_text(path.joinpath(name), normalize='NFC').replace('\n', '')

    diacritics = _read_string('diacritics').replace('-', '')
    vowels = ''.join(v for v in _read_string('vowels') if v not in diacritics)
    return diacritics, vowels, _read_string('tones')


@implementer(ISoundClassModel)
class SoundClassModel(NamedObject):
    def __init__(self, name, converter, scorer, vowels, tones, info):
        NamedObject.__init__(self, name)
        self.scorer = scorer
        self.converter = converter
        self.vowels = vowels
        self.tones = tones
        self.info = info

    @classmethod
    def from_path(cls, path):
        assert path.is_dir()
        cache = Cache()

        def cache_key(suffix):
            return '.'.join(['SoundClassModel', as_unicode(path.name), suffix])

        if cache_key('converter') not in cache:
            cache[cache_key('converter')] = _read_converter(path.joinpath('converter'))
        converter = cache[cache_key('converter')]

        if cache_key('scorer') not in cache:
            cache[cache_key('scorer')] = _read_scorer(path)
        scorer = cache[cache_key('scorer')]

        # read information from the info-file
        info = {k: ''
                for k in ['description', 'compiler', 'source', 'date', 'vowels', 'tones']}
        meta_pattern = re.compile('@(?P<key>[^:]+):\s*(?P<value>.*)')
        for line in read_lines(path.joinpath('INFO')):
            match = meta_pattern.match(line)
            if match:
                info[match.group('key')] = match.group('value')

        return cls(
            as_unicode(path.name), converter, scorer, info['vowels'], info['tones'], info)

    def __getitem__(self, x):
        return self.converter[x]

    def __contains__(self, x):
        return x in self.converter

    def __call__(self, x, y):
        """
        Use the call-shortcut to retrieve the scoring function.
        """
        return self.scorer[x, y]

    def __unicode__(self):
        return """\
Model:    {0}
Info:     {1}
Source:   {2}
Compiler: {3}
Date:     {4}
""".format(
            self.name,
            self.info.get('description'),
            self.info.get('source'),
            self.info.get('compiler'),
            self.info.get('date')
        )


def read_items(path):
    for line in read_lines(path, normalize='NFC'):
        key, values = line.split(' : ')
        yield key, values.split(', ')


def _read_converter(path):
    """
    Function imports individually defined sound classes from a text file and
    creates a replacement dictionary from these sound classes.
    """
    converter, errors = {}, []

    for key, values in read_items(path):
        for value in values:
            log.debug('%s' % ((value, key),))
            if converter.setdefault(value, key) != key:  # pragma: no cover
                errors.append(value)
    if errors:  # pragma: no cover
        log.debug("Values {0} in file {1} are multiply defined!".format(
            ' // '.join(uniq(errors)), path))
        raise ValueError("invalid converter spec")
    return converter


def read_scorer(path):
    """
    Read a scoring function in a file into a ScoreDict object.

    Parameters
    ----------
    path : Path
        The path to the input file that shall be read as a scoring dictionary.
        The matrix format is a simple csv-file in which the scoring matrix is
        displayed, with negative values indicating high differences between
        sound segments (or sound classes) and positive values indicating high
        similarity. The matrix should be symmetric, columns should be separated
        by tabstops, and the first column should provide the alphabet for which
        the scoring function is defined.

    Returns
    -------
    scoredict : ~lingpy.algorithm.ScoreDict
        A ScoreDict instance which can be directly passed to LingPy's alignment
        functions.
    """
    chars, matrix = [], []
    for row in reader(path, delimiter='\t'):
        if row:
            chars.append(row[0])
            matrix.append(map(float, row[1:]))
    return ScoreDict(chars, matrix)


def _read_scorer(path):
    # try to load the scoring function or the score tree
    matrix = path.joinpath('matrix')
    if matrix.is_file():
        return read_scorer(matrix)
    if path.joinpath('scorer').is_file():
        score_tree = ScoreTree(list(read_items(path.joinpath('scorer'))))
        return score_tree.get_scoredict()

    return ScoreDict([], [])

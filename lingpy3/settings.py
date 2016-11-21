# coding: utf8
from __future__ import unicode_literals, print_function, division

import attr
from zope.interface import implementer
from clldutils.misc import UnicodeMixin

from lingpy3.interfaces import ILexstatSettings, IAlignmentSettings


class Settings(UnicodeMixin):
    def asdict(self):
        return attr.asdict(self)


@attr.s
@implementer(ILexstatSettings)
class LexstatSettings(Settings):
    transform = attr.ib(default={
        'A': 'C',
        'B': 'C',
        'C': 'C',
        'L': 'c',
        'M': 'c',
        'N': 'c',
        'X': 'V',
        'Y': 'V',
        'Z': 'V',
        'T': 'T',
        '_': '_'})
    runs = attr.ib(default=1000),
    modes = attr.ib(default=[("global", -2, 0.5), ("local", -1, 0.5)]),
    rands = attr.ib(default=1000),
    limit = attr.ib(default=10000),
    scoring_method = attr.ib(default='shuffle'),
    ratio = attr.ib(default=(2, 1)),
    vscale = attr.ib(default=1.0),
    threshold = attr.ib(default=0.45),
    cluster_method = attr.ib(default='upgma'),
    preprocessing_method = attr.ib(default='sca'),
    preprocessing_threshold = attr.ib(default=0.7),
    bad_chars_limit = attr.ib(default=0.1),
    scoring_threshold = attr.ib(default=0.7)


@attr.s
@implementer(IAlignmentSettings)
class AlignmentSettings(Settings):
    mode = attr.ib(default='global'),
    modes = attr.ib(default=[('global', -2, 0.5), ('local', -1, 0.5)]),
    scale = attr.ib(default=0.5),
    factor = attr.ib(default=0.3),
    gap_weight = attr.ib(default=0.5),
    classes = attr.ib(default=True),
    sonar = attr.ib(default=True),
    scorer = attr.ib(default={}),
    tree_calc = attr.ib(default='neighbor'),
    gop = attr.ib(default=-2),
    transform = attr.ib(default={
        # new values for alternative prostrings
        'A': 1.6,  # initial
        'B': 1.3,  # syllable-initial
        'C': 1.2,  # ascending
        'L': 1.1,  # descending
        'M': 1.1,  # syllable-descending
        'N': 0.5,  # final
        'X': 3.0,  # vowel in initial syllable
        'Y': 3.0,  # vowel in non-final syllable
        'Z': 0.7,  # vowel in final syllable
        'T': 1.0,  # Tone
        '_': 0.0  # break character
    }),
    notransform = attr.ib(default={
        # new values for alternative prostrings
        'A': 1,  # initial
        'B': 1,  # syllable-initial
        'C': 1,  # ascending
        'L': 1,  # descending
        'M': 1,  # syllable-descending
        'N': 1,  # final
        'X': 1,  # vowel in initial syllable
        'Y': 1,  # vowel in non-final syllable
        'Z': 1,  # vowel in final syllable
        'T': 1,  # Tone
        '_': 1  # break character
    }),
    stamp = attr.ib(default="""# MSA
# dataset    : {0}
# collection : {1}
# aligned by : {2}
# created on : {3}
# parameters : {4}
""")

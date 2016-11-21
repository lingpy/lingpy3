# coding: utf8
from __future__ import unicode_literals, print_function, division

from lingpy3 import registry
from lingpy3.sequence.soundclassmodel import SoundClassModel, DiacriticsVowelsTones
from lingpy3 import settings

__version__ = "1.0"
PROG = 'LingPy3-{0}'.format(__version__)

for name in ['asjp', 'dolgo', 'art', 'sca', 'color', 'cv', 'jaeger']:
    registry.register(SoundClassModel.from_name(name))

for name in ['dvt', 'dvt_el']:
    registry.register(DiacriticsVowelsTones.from_name(name))

registry.register(settings.LexstatSettings())
registry.register(settings.AlignmentSettings())

"""
Package for specific algorithms and time-intensive routines.
"""
# flake8: noqa
#from lingpy.algorithm._tree import _TreeDist as TreeDist
from six import PY2

cmod = set()
try:
    from lingpy3.algorithm.cython import calign as calign
except ImportError:  # pragma: no cover
    from lingpy3.algorithm.cython import _calign as calign
    cmod.add('calign')

try:
    from lingpy3.algorithm.cython import malign as malign
except ImportError:  # pragma: no cover
    from lingpy3.algorithm.cython import _malign as malign
    cmod.add('malign')

try:
    from lingpy3.algorithm.cython import talign as talign
except ImportError:  # pragma: no cover
    from lingpy3.algorithm.cython import _talign as talign
    cmod.add('talign')

try:
    from lingpy3.algorithm.cython import misc as misc
except IndexError:  # pragma: no cover
    from lingpy3.algorithm.cython import _misc as misc
    cmod.add('misc')

# define squareform for global lingpy-applications
squareform = misc.squareform


class ScoreDict(misc.ScoreDict):
    def __init__(self, chars, matrix):
        if PY2:
            chars = [c.encode('utf8') for c in chars]
        misc.ScoreDict.__init__(self, chars, matrix)

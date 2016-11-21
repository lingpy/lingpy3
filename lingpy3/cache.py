# *-* coding: utf-8 *-*
"""Implements the lingpy cache.

Some operations in lingpy may be time consuming, so we provide a mechanism to cache the
results of these operations.
"""
from __future__ import unicode_literals, print_function, absolute_import, division
import pickle

import appdirs
from clldutils.path import Path, remove, path_component, as_unicode

CACHE_DIR = appdirs.user_cache_dir(__name__.split('.')[0])


class Cache(object):
    def __init__(self, dir_=None):
        self._dir = Path(dir_ or CACHE_DIR)
        if not self._dir.exists():
            self._dir.mkdir(parents=True)  # pragma: no cover

    def _path(self, key):
        return self._dir.joinpath(path_component(key))

    def __len__(self):
        return len(list(self.keys()))

    def __getitem__(self, item):
        with self._path(item).open('rb') as fp:
            return pickle.load(fp)

    def __setitem__(self, key, value):
        with self._path(key).open('wb') as fp:
            pickle.dump(value, fp)

    def __delitem__(self, key):
        remove(self._path(key))

    def __contains__(self, item):
        return self._path(item).exists()

    def keys(self):
        for p in self._dir.iterdir():
            yield as_unicode(p.name)

    def clear(self):
        for key in self.keys():
            remove(self._path(key))

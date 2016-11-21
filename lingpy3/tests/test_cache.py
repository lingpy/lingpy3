# coding: utf8
from __future__ import unicode_literals, print_function, division

from clldutils.testing import WithTempDir


class TestCache(WithTempDir):
    def test_cache(self):
        from lingpy3.cache import Cache

        cache = Cache(self.tmp_path('cache'))
        key, obj = 'töst', {'a': 123}
        self.assertNotIn(key, cache)
        cache[key] = obj
        self.assertEqual(cache[key]['a'], 123)
        del cache[key]
        self.assertEqual(len(cache), 0)
        cache[key] = obj
        cache.clear()
        self.assertEqual(len(cache), 0)

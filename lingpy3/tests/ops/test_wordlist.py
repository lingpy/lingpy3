# coding: utf8
from __future__ import unicode_literals, print_function, division
from unittest import TestCase

from lingpy3.tests.fixtures import make_wordlist


class Tests(TestCase):
    def test_distances(self):
        from lingpy3.ops.wordlist import distances

        wl = make_wordlist()
        self.assertEquals(
            distances(wl),
            [
                [0, 1.0, 0.5, 1.0, 0.5],
                [1.0, 0, 1.0, 0.0, 1.0],
                [0.5, 1.0, 0, 1.0, 0.0],
                [1.0, 0.0, 1.0, 0, 1.0],
                [0.5, 1.0, 0.0, 1.0, 0]
            ])

        self.assertEquals(
            distances(wl, mode='jaccard'),
            [
                [0, 1.0, 0.75, 1.0, 0.75],
                [1.0, 0, 0.8, 0.0, 0.8],
                [0.75, 0.8, 0, 0.8, 0.0],
                [1.0, 0.0, 0.8, 0, 0.8],
                [0.75, 0.8, 0.0, 0.8, 0]
            ])

        distances(wl, mode='shared', refB='x')

        # No shared concepts between languages:
        rows = [
            ['1', 'l1', 'hand', 'hand', 'a', 'abera'],
            ['2', 'l2', 'arm', 'arm', 'b', 'aberb'],
        ]
        distances(make_wordlist(rows=rows))

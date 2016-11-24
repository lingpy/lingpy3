# coding: utf8
from __future__ import unicode_literals, print_function, division
from unittest import TestCase

from lingpy3.sequence.soundclassmodel import read_items
from lingpy3.util import data_path


class Tests(TestCase):
    def test_ScoreTree(self):
        from lingpy3.sequence.scoretree import ScoreTree

        tree = ScoreTree([('A', ['g', 'C:1']), ('C', ['c', 'A:4'])])
        tree.get_scoredict()

        tree = ScoreTree(list(read_items(data_path('models', 'sca', 'scorer'))))
        sd = tree.get_scoredict()
        self.assertEqual(
            sd.matrix[20],
            [-100.0, 0.0, -20.0, -20.0, -20.0, -20.0, -20.0, -20.0, 9.0, -10.0, 0.0, 0.0,
             0.0, -10.0, 0.0, 0.0, -10.0, 0.0, 0.0, 0.0, 10.0, 1.0, -10.0, 0.0, 0.0, 0.0,
             0.0, -10.0, 0.0, 0.0, -10.0, -10.0])

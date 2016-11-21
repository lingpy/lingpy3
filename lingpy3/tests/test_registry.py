# coding: utf8
from __future__ import unicode_literals, print_function, division
from unittest import TestCase

from zope.interface.verify import DoesNotImplement


class Tests(TestCase):
    def test_register(self):
        from lingpy3.registry import register, get
        from lingpy3.interfaces import ISoundClassModel
        from lingpy3.sequence.soundclassmodel import SoundClassModel

        with self.assertRaises(DoesNotImplement):
            register(None, ISoundClassModel)

        register(SoundClassModel('test', {}, {}, '', '', {}))
        self.assertEqual(get(ISoundClassModel, 'test').name, 'test')

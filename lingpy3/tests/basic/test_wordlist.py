# coding: utf8
from __future__ import unicode_literals, print_function, division
from unittest import TestCase


class Tests(TestCase):
    def _make_one(self, header=None, rows=None, **kw):
        from lingpy3.basic.wordlist import Wordlist

        _header = ['id', 'doculect', 'concept', 'ipa', 'cognates', 'x']
        _rows = [
            ['1', 'l1', 'hand, arm', 'aber', 'a', 'abera'],
            ['2', 'l2', 'hand, arm', 'aber', 'b', 'aberb'],
            ['3', 'l3', 'hand, arm', 'aba', 'a', 'abaa'],
            ['4', 'l4', 'hand, arm', 'abra kadabra', 'b', 'abra kadabrab'],
            ['5', 'l5', 'hand, arm', 'test\u201dtest', 'a', 'test\u201dtesta'],
            ['6', 'l1', 'foot', 'was', 'a', 'wasa'],
            ['7', 'l2', 'foot', 'den', 'fb', 'denfb'],
            ['8', 'l3', 'foot', 'hier', 'fa', 'hierfa'],
            ['9', 'l4', 'foot', 'fu\xdf', 'fb', 'fu\xdffb'],
            ['10', 'l5', 'foot', 'haut', 'fa', 'hautfa'],
            ['11', 'l1', 'knee', 'Knie', 'gc', 'Kniegc'],
        ]

        return Wordlist(
            _header if header is None else header, _rows if rows is None else rows, **kw)

    def test_init(self):
        self._make_one()

        # invalid data type for header:
        with self.assertRaises(ValueError):
            self._make_one(header=['id', 'concept', 'doculect', 5])

        # duplicate column names in header:
        with self.assertRaises(ValueError):
            self._make_one(header=['id', 'concept', 'doculect', 'id'])

        # missing columns in header:
        with self.assertRaises(ValueError):
            self._make_one(header=[])

        # row length not matching header length:
        with self.assertRaises(ValueError):
            self._make_one(rows=[[1, 2]])

        # duplicate row ID:
        with self.assertRaises(ValueError):
            self._make_one(rows=[[1, 2, 3], [1, 2, 3]])

    def test_get_etymdict(self):
        wl = self._make_one()
        self.assertEqual(
            wl.get_etymdict(ref='concept'),
            {
                'foot': [['6'], ['7'], ['8'], ['9'], ['10']],
                'hand, arm': [['1'], ['2'], ['3'], ['4'], ['5']],
                'knee': [['11'], [], [], [], []]})

    def test_iter_paps(self):
        wl = self._make_one()
        self.assertEqual(
            list(wl.iter_paps(ref='cognates', missing=-1)),
            [
                ('a', [1, 1, 1, 1, 1]),
                ('b', [0, 1, 0, 1, 0]),
                ('fa', [0, 0, 1, 0, 1]),
                ('fb', [0, 1, 0, 1, 0]),
                ('gc', [1, -1, -1, -1, -1])
            ])

    def test_add_col(self):
        wl = self._make_one()

        with self.assertRaises(ValueError):
            wl.add_col('id', lambda x: 'x')

        wl.add_col('xcol', lambda x: 'x')
        self.assertEqual(wl['1', 'xcol'], 'x')
        self.assertEqual(wl.header[-1], 'xcol')

        with self.assertRaises(ValueError):
            wl.add_col('xcol', lambda x: 'x')

        wl.add_col('xcol', lambda x: 'y', override=True)
        self.assertEqual(wl['1', 'xcol'], 'y')

        wl.add_col('zcol', lambda x: x['xcol'])
        self.assertEqual(wl['1', 'zcol'], 'y')
        wl['1', 'xcol'] = 'z'
        self.assertEqual(wl['1', 'xcol'], 'z')

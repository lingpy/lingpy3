# coding: utf8
from __future__ import unicode_literals, print_function, division

from lingpy3.basic.wordlist import Wordlist


def make_wordlist(header=None, rows=None, **kw):
    _header = ['id', 'doculect', 'concept', 'ipa', 'cogid', 'x']
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

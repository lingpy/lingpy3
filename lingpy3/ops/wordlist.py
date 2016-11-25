# coding: utf8
from __future__ import unicode_literals, print_function, division
from collections import defaultdict

from lingpy3.ops.base import operation
from lingpy3.interfaces import IWordlist
from lingpy3.util import product2, chained_values
from lingpy3 import log


def get_score(wl, ref, mode, taxA, taxB, ignore_missing=False):
    refsA, refsB = defaultdict(list), defaultdict(list)
    for concept, items in wl.iter_by_concept('language', ref):
        refsA[concept] = [r for lang, r in items if lang == taxA] or [0]
        refsB[concept] = [r for lang, r in items if lang == taxB] or [0]

    if mode in ['shared', 'jaccard']:
        listA = chained_values(refsA)
        listB = chained_values(refsB)
        shared = [x for x in listA if x in listB]

        if mode == 'jaccard':
            return 1 - len(set(shared)) / len(set(listA + listB))
        return len(shared)

    assert mode == 'swadesh'
    # count amount of shared concepts
    shared, missing = 0, 0

    for concept in wl.concepts:
        if refsA.get(concept) == [0] or refsB.get(concept) == [0]:
            missing += 1 if not ignore_missing else 0
        elif [k for k in refsA[concept] if k in refsB[concept]]:
            shared += 1

    try:
        return 1 - shared / (len(wl.concepts) - missing)
    except ZeroDivisionError:
        log.get_logger().exception(
            "Zero-division error encountered in '{0}' and '{1}'.".format(taxA, taxB))
        return 1.0


@operation(IWordlist)
def distances(wl, ref='cogid', refB='', mode='swadesh', ignore_missing=False, **kw):
    """
    Compute a distance matrix from a wordlist.

    :param ref:
    :param refB:
    :param mode:
    :param ignore_missing:
    :param kw:
    :return:
    """
    dists = [[0 for _ in range(len(wl.languages))] for _ in range(len(wl.languages))]

    for (i, taxA), (j, taxB) in product2(enumerate(wl.languages)):
        if i < j:
            score = get_score(wl, ref, mode, taxA, taxB, ignore_missing=ignore_missing)
            dists[i][j] = score
            if not refB:
                dists[j][i] = score
        elif i == j:
            if mode == 'shared':
                dists[i][j] = len(chained_values(wl.get_dict_by_concept(language=taxA)))
        elif i > j and refB:
            dists[i][j] = get_score(
                wl, refB, mode, taxA, taxB, ignore_missing=ignore_missing)

    return dists

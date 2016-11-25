# coding: utf8
from __future__ import unicode_literals, print_function, division

from clldutils.dsv import UnicodeWriter

from lingpy3.io.writer.base import writer
from lingpy3.interfaces import IWordlist


@writer(IWordlist)
def csv(wl, delimiter='\t', **kw):
    with UnicodeWriter(f=None, delimiter=delimiter, **kw) as writer:
        writer.writerow(wl.header)
        for row in wl:
            writer.writerow(row)
    return writer.read().decode('utf8')


@writer(IWordlist)
def paps_nex(wl, **kw):
    missing = kw.pop('missing', 0)
    paps = sorted(wl.iter_paps(
        ref=kw.pop('ref', 'cogid'),
        concept=kw.pop('concept', None),
        missing=missing))

    template = """\
#NEXUS

BEGIN DATA;
DIMENSIONS ntax={0} NCHAR={1};
FORMAT DATATYPE=STANDARD GAP=- MISSING={2} interleave=yes;
MATRIX

{3}
;

END;
[PAPS-REFERENCE]
{4}
"""

    max_taxon = max([len(taxon) for taxon in wl.languages])
    matrix = []
    for i, taxon in enumerate(wl.languages):
        matrix.append(('{0:%s} {1}' % max_taxon).format(
            taxon, ''.join('%s' % itm[i] for _, itm in paps)))

    return template.format(
        len(wl.languages),
        len(paps),
        missing,
        '\n'.join(matrix),
        '\n'.join('[{0} :: {1}]'.format(i, ref) for i, (ref, _) in enumerate(paps))
    )

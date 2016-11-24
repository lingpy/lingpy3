# coding: utf8
from __future__ import unicode_literals, print_function, division

from zope.component import adapts
from clldutils.dsv import UnicodeWriter

from lingpy3.io.writer.base import BaseWriter
from lingpy3.interfaces import IWordlist


class Csv(BaseWriter):
    name = 'csv'
    adapts(IWordlist)

    def get(self, **kw):
        with UnicodeWriter(f=None, delimiter=kw.get('delimiter', '\t')) as writer:
            writer.writerow(self.obj.header)
            for row in self.obj:
                writer.writerow(row)
        return writer.read().decode('utf8')


class PapsNex(BaseWriter):
    name = 'paps.nex'
    adapts(IWordlist)

    def get(self, **kw):
        missing = kw.pop('missing', 0)
        paps = sorted(self.obj.iter_paps(
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

        max_taxon = max([len(taxon) for taxon in self.obj.languages])
        matrix = []
        for i, taxon in enumerate(self.obj.languages):
            matrix.append(('{0:%s} {1}' % max_taxon).format(
                taxon, ''.join('%s' % itm[i] for _, itm in paps)))

        return template.format(
            len(self.obj.languages),
            len(paps),
            missing,
            '\n'.join(matrix),
            '\n'.join('[{0} :: {1}]'.format(i, ref) for i, (ref, _) in enumerate(paps))
        )

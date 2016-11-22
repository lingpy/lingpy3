# coding: utf8
from __future__ import unicode_literals, print_function, division
from itertools import groupby
from operator import itemgetter

from six import text_type
from clldutils.misc import cached_property

from lingpy3.util import uniq


def split(value):
    return value.split()


def join(values):
    return ' '.join(values)


class Wordlist(object):
    def __init__(self, header, rows, id_='id', concept='concept', language='doculect'):
        """
        Initialize a Wordlist object.

        :param header: `list` of column headers.
        :param rows: `list` of `list`s, constituting the body of the wordlist.
        :param id_: Name of the column to regard as ID.
        :param concept: Name of the column storing the concept ID.
        :param language: Name of the column storing the language ID.
        """
        # For performance reasons we store a wordlist as list of lists, rather than as
        # list of OrderedDicts. To allow dict-like access, we have to compute (and
        # possibly update) indexes to map row IDs to list indices and column names to
        # list indices.

        if len(set(header)) != len(header):
            raise ValueError('column names must be unique')
        if not all(isinstance(col, text_type) for col in header):
            raise ValueError('column names must be unicode')
        if not all(col in header for col in [id_, language, concept]):
            raise ValueError('id_, concept and language columns must be present')
        self._rows = []
        for row in rows:
            if not (isinstance(row, (tuple, list)) and len(row) == len(header)):
                raise ValueError('rows must be lists of same length as the header')
            self._rows.append(list(row))
        self.concept_col = concept
        self.language_col = language
        self.id_col = id_

        # Map header names to list index in self.header:
        self._header2index = {h: i for i, h in enumerate(header)}

        # Map row IDs to list index in self._rows:
        id_index = self._header2index.get(id_, 0)
        self._id2index = {row[id_index]: i for i, row in enumerate(self._rows)}

        # Make sure row IDs are unique:
        if len(self._id2index) != len(self._rows):
            raise ValueError('duplicate row IDs in wordlist')

    def _row_index(self, row):
        """
        :param row: int or text_type, specifying 1-based row index or row ID.
        :return: list index
        """
        return row - 1 if isinstance(row, int) else self._id2index[row]

    def _col_index(self, col):
        """
        :param col: int or text_type, specifying 1-based column index or column name.
        :return: list index
        """
        _map = {'concept': self.concept_col, 'language': self.language_col}
        return col - 1 if isinstance(col, int) else self._header2index[_map.get(col, col)]

    def __iter__(self):
        """
        Iterating over a wordlist means iterating over its rows.
        """
        return iter(self._rows)

    @property
    def header(self):
        return [col for col, i in sorted(self._header2index.items(), key=itemgetter(1))]

    @cached_property()
    def languages(self):
        """
        :return: `list` of unique language identifiers used in the wordlist.
        """
        return self.get_distinct(self.language_col)

    @cached_property()
    def concepts(self):
        """
        :return: `list` of unique concept identifiers used in the wordlist.
        """
        return self.get_distinct(self.concept_col)

    def __getitem__(self, item):
        if isinstance(item, tuple):
            assert len(item) == 2
            return self._rows[self._row_index(item[0])][self._col_index(item[1])]
        return self._rows[self._row_index(item)]

    def iter_slices(self, cols, rows=None):
        """
        Iterate over rows or the whole wordlist, yielding slices of each row.

        :param cols: `list` of columns to include in each slice.
        :param rows: Iterable of rows
        :return: Generator object.
        """
        if not isinstance(cols, (list, tuple)):
            cols = [cols]
        rows = rows or self
        cols = [self._col_index(col) for col in cols]
        if len(cols) == 0:
            return rows
        if len(cols) == 1:
            return (r[cols[0]] for r in rows)
        return ([r[col] for col in cols] for r in rows)

    def get_slices(self, cols, rows=None):
        """
        Slice values specified by `cols` out of rows.

        :param cols:
        :param rows:
        :return: `list` of slices
        """
        return list(self.iter_slices(cols, rows=rows))

    def filter(self, **query):
        """
        Filter wordlist rows based on criteria for values.

        :param query: Filter criteria keyed by column name.
        :return: generator object.
        """
        query = [(self._col_index(col), q) for col, q in query.items()]
        return (row for row in self if all(row[col] == q for col, q in query))

    def get_distinct(self, *cols):
        """
        :param cols: slice specification.
        :return: `list` of distinct slices.
        """
        return uniq(self.iter_slices(cols))

    def iter_grouped(self, key, *cols, **query):
        """
        Iterate over lists of slices grouped by value for the column specified as `key`.

        :param key:
        :param cols: slice specification.
        :param query: filter specification.
        :return: Generator of (key, slices) pairs.
        """
        if not isinstance(key, int):
            key = self._header2index[key]
        for k, rows in groupby(
                sorted(self.filter(**query) if query else self, key=lambda r: r[key]),
                lambda r: r[key]):
            yield k, list(self.iter_slices(cols, rows=rows))

    def iter_by_language(self, *cols, **query):
        return self.iter_grouped(self.language_col, *cols, **query)

    def get_by_language(self, *cols, **query):
        return list(self.iter_by_language(*cols, **query))

    def get_dict_by_language(self, *cols, **query):
        return {k: items for k, items in self.iter_by_language(*cols, **query)}

    def iter_by_concept(self, *cols, **query):
        return self.iter_grouped(self.concept_col, *cols, **query)

    def get_by_concept(self, *cols, **query):
        return list(self.iter_by_concept(*cols, **query))

    def get_dict_by_concept(self, *cols, **query):
        return {k: items for k, items in self.iter_by_concept(*cols, **query)}

    def add_col(self, col, func, override=False, **kw):
        """
        Add a column to all rows in the wordlist.

        :param col: The name of the new column.
        :param func: A callable accepting a row represented as dict, returning the \
        value for the new column for the row.
        """
        assert isinstance(col, text_type)
        if col in [self.id_col, self.concept_col, self.language_col]:
            raise ValueError('cannot overwrite values of reserved columns')

        index = self._header2index.get(col)
        if index is not None:
            if not override:
                raise ValueError('to overwrite existing columns, specify `override=True`')
        else:
            self._header2index[col] = index = len(self._header2index)
        header = self.header
        for i, row in enumerate(self):
            self._rows[i].insert(index, func(dict(zip(header, row)), **kw))

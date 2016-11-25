# coding: utf8
from __future__ import unicode_literals, print_function, division
from zope.interface import Interface, Attribute


class IPath(Interface):
    """"""


class IText(Interface):
    """"""


class IOperation(Interface):
    """"""
    def __call__(self, **kw):
        """"""


class IWordlist(Interface):
    """

    """
    concept_col = Attribute("""""")
    language_col = Attribute("""""")
    id_col = Attribute("""""")
    header = Attribute("""""")
    languages = Attribute("""""")
    concepts = Attribute("""""")

    def __len__(self):
        """"""

    def __iter__(self):
        """"""


class IWriter(Interface):
    """"""
    def get(self, **kw):
        """"""

    def write(self, path, **kw):
        """"""


class ISoundClassModel(Interface):
    """
    Interface for sound-class models.
    """
    name = Attribute("""\
        The name of the model.""")
    converter = Attribute("""\
        A dictionary with IPA tokens as keys and sound-class characters as values.""")
    scorer = Attribute("""\
        A scoring dictionary with tuples of sound-class characters as keys and
        similarity scores as values.""")
    info = Attribute("""\
        A dictionary storing the key-value pairs defined in the ``INFO``.""")
    __getitem__ = Attribute("""""")
    __contains__ = Attribute("""""")


class IDiactriticsVowelsTones(Interface):
    """
    """


class ILexstatSettings(Interface):
    """
    """
    asdict = Attribute("""""")


class IAlignmentSettings(Interface):
    """
    """
    asdict = Attribute("""""")

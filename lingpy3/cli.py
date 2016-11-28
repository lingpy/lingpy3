# *-* coding: utf-8 *-*
from __future__ import print_function, division, unicode_literals
import argparse

from six import with_metaclass, text_type
from clldutils.path import Path, path_component, as_unicode

from lingpy3.ops import run
from lingpy3.io import read
from lingpy3 import interfaces
from lingpy3 import jsonlib


class CommandMeta(type):
    """
    A metaclass which keeps track of subclasses with all-lowercase names.
    """
    __instances = []

    def __init__(self, name, bases, dct):
        super(CommandMeta, self).__init__(name, bases, dct)
        if name == name.lower():
            self.__instances.append(self)

    def __iter__(self):
        return iter(self.__instances)


class Command(with_metaclass(CommandMeta, object)):
    """Base class for subcommands of the lingpy command line interface."""
    help = None

    @classmethod
    def subparser(cls, parser):
        """Hook to define subcommand arguments."""
        return  # pragma: no cover

    def __call__(self, args):
        """Hook to run the subcommand."""
        raise NotImplemented()  # pragma: no cover


def _cmd_by_name(name):
    for cmd in Command:
        if cmd.__name__ == name:
            return cmd()


class help(Command):
    """
    Show help for commands.
    """

    @classmethod
    def subparser(self, parser):
        parser.add_argument(
            'cmd', choices=[cmd.__name__ for cmd in Command if cmd.__name__ != 'help'])

    def __call__(self, args):
        cmd = _cmd_by_name(args.cmd)
        if cmd.__doc__:
            print('\n%s\n' % cmd.__doc__.strip())
        print(cmd.help)  # pragma: no cover


def _args_kw(s):
    args, kw = s.split(':'), {}
    if len(args) > 1 and '=' in args[-1]:
        kw = {k.split('=')[0]: k.split('=')[1] for k in args.pop().split(';')}
    return args, kw


class operation(Command):
    """
    Run any lingpy3 operation.
    """
    @classmethod
    def subparser(cls, p):
        p.add_argument('name')
        p.add_argument('object')

    def __call__(self, args):
        opargs, opkw = _args_kw(args.name)
        readargs, readkw = _args_kw(args.object)
        oname, if_, input_ = readargs
        input_ = text_type(input_)
        if Path(path_component(input_)).exists():
            # We heuristically interpret the input as filename, if a file with that name
            # exists.
            input_ = Path(path_component(input_))
        res = run(
            opargs[0],
            read(oname, getattr(interfaces, if_), input_, **readkw),
            **opkw)
        p = jsonlib.dump(res, outdir=Path(args.output))
        print('Result written to <%s>' % as_unicode(p))
        return p


def get_parser():
    # basic parser for lingpy
    parser = argparse.ArgumentParser(
        description=main.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--verbose', '-v', default=False, help='Verbose output')
    parser.add_argument('--output', '-o', default='.', help='Output directory')

    subparsers = parser.add_subparsers(dest="subcommand")
    for cmd in Command:
        subparser = subparsers.add_parser(
            cmd.__name__,
            help=(cmd.__doc__ or '').strip().split('\n')[0],
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        cmd.subparser(subparser)
        cmd.help = subparser.format_help()

    return parser


def main(*args):
    """
    LingPy3 command line interface.
    """
    args = get_parser().parse_args(args or None)
    return _cmd_by_name(args.subcommand)(args)

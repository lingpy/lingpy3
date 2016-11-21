# *-* coding: utf-8 *-*
"""Configuration management for lingpy.

Various aspects of lingpy can be configured and customized by the user. This is done with
configuration files in the user's config dir.

.. seealso:: https://pypi.python.org/pypi/appdirs/
"""
from __future__ import unicode_literals, print_function, absolute_import, division
from collections import OrderedDict

from six import text_type
import appdirs
from clldutils.path import Path
from clldutils.inifile import INI

CONFIG_DIR = appdirs.user_config_dir(__name__.split('.')[0])


class Config(INI):
    def __init__(self, name, dir_=None, default=None, **kw):
        """Initialization.

        :param name: Basename for the config file (suffix .ini will be appended).
        :param default: Default content of the config file.
        """
        INI.__init__(self, kw, allow_no_value=True)
        self.name = name
        config_dir = Path(dir_ or CONFIG_DIR)

        if default:
            if isinstance(default, text_type):
                self.read_string(default)
            #elif isinstance(default, (dict, OrderedDict)):
            #    self.read_dict(default)

        cfg_path = config_dir.joinpath(name + '.ini')
        if cfg_path.exists():
            assert cfg_path.is_file()
            self.read(cfg_path.as_posix())
        else:
            if not config_dir.exists():
                try:
                    config_dir.mkdir()
                except OSError:  # pragma: no cover
                    # this happens when run on travis-ci, by a system user.
                    pass
            if config_dir.exists():
                self.write(cfg_path.as_posix())
        self.path = cfg_path

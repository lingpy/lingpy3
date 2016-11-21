from __future__ import unicode_literals

from clldutils.testing import WithTempDir
from clldutils.inifile import INI

from lingpy3.config import Config


class ConfigTest(WithTempDir):
    def test_new_config(self):
        dir_ = self.tmp_path('.config')
        self.assertFalse(dir_.exists())
        Config('test', dir_=dir_)
        self.assertTrue(dir_.exists())

    def test_existing_config(self):
        cfg = INI()
        cfg.read_dict({'section': {'option': '12'}})
        cfg.write(self.tmp_path('test.ini'))
        cfg = Config('test', dir_=self.tmp_path())
        self.assertEqual(cfg.get('section', 'option'), '12')

    def test_default(self):
        cfg = Config('test', dir_=self.tmp_path(), default="""\
[section2]
option2 = 7
""")
        self.assertEqual(cfg.get('section2', 'option2'), '7')

# coding: utf8
from __future__ import unicode_literals, print_function, division
import logging

from clldutils.testing import WithTempDir, capture_all

from lingpy3 import log


class LogTest(WithTempDir):
    def tearDown(self):
        # Reset the global _logger to make sure, it's recreated with appropriate config
        # when the other tests are run.
        log._logger = None
        WithTempDir.tearDown(self)

    def test_Logging_context_manager(self):
        #
        # Note: We must make sure to acquire a fresh logger *within* the capture_all
        # context, because otherwise, stderr redirection won't work. Thus, we have to
        # initialize the logger and call one of its logging methods within one function
        # which we will then pass to capture_all.
        #
        def _log(method='debug', with_context_manager=False, level=logging.DEBUG):
            logger = log.get_logger(
                test=True, force_default_config=True, config_dir=self.tmp_path())
            method = getattr(logger, method)
            if with_context_manager:
                with log.Logging(logger=logger, level=level):
                    method('', extra=dict(lines=['a', 'ä']))
            else:
                method('')

        with capture_all(_log, with_context_manager=False) as res:
            self.assertNotIn('DEBUG', res[2])

        with capture_all(_log, with_context_manager=True) as res:
            self.assertIn('DEBUG', res[2])

        with capture_all(_log, with_context_manager=True, level=logging.WARN) as res:
            self.assertNotIn('DEBUG', res[2])

        with capture_all(
            _log, method='warn', with_context_manager=True, level=logging.WARN
        ) as res:
            self.assertIn('WARN', res[2])

    def test_new_config(self):
        l = log.get_logger(config_dir=self.tmp.as_posix(), test=True)
        self.assertTrue(hasattr(l, 'info'))
        self.assertEqual(log.get_level(), logging.INFO)

    def test_default_config(self):
        l = log.get_logger(config_dir=self.tmp.as_posix(), force_default_config=True)
        self.assertTrue(hasattr(l, 'info'))

    def test_convenience(self):
        log.info('m')
        log.warn('m')
        log.debug('m')
        log.error('m')
        log.deprecated('o', 'n')
        log.missing_module('m')
        log.file_written('f')

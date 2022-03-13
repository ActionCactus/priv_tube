from unittest import TestCase
import pytest
import logging
import os

from priv_tube.core.boot.initialization_routines.configure_logger import ConfigureLogger
from priv_tube.core.exceptions import SystemConfigurationError

logger = logging.getLogger(__name__)


class ConfigureLoggerTest(TestCase):
    def test_resolving_log_level_with_env_variable(self):
        os.environ["LOG_LEVEL"] = "warning"
        ConfigureLogger().run()
        assert logging.getLogger().level == logging.WARNING

    def test_resolving_log_level_with_bad_env_variable_raises_an_error(self):
        os.environ["LOG_LEVEL"] = "an invalid log level"
        with pytest.raises(SystemConfigurationError):
            ConfigureLogger().run()

    def test_resolving_log_level_without_env_variable_uses_default(self):
        os.environ.pop("LOG_LEVEL")
        ConfigureLogger().run()
        assert logging.getLogger().level

    def test_resolving_log_formatter_with_env_variable(self):
        os.environ["LOG_FORMATTER"] = "colorized"
        ConfigureLogger().run()
        # Just run it to make sure it can complete without error.

    def test_resolving_log_formatter_with_bad_env_variable_raises_an_error(self):
        os.environ["LOG_FORMATTER"] = "an invalid log formatter"
        with pytest.raises(SystemConfigurationError):
            ConfigureLogger().run()

    def test_resolving_log_formatter_without_env_variable_uses_default(self):
        ConfigureLogger().run()
        default_logger = logging.getLogger()
        assert default_logger.hasHandlers()


@pytest.mark.parametrize(
    "ll_env,lf_env,func",
    [
        ("debug", "colorized", logger.debug),
        ("debug", "colorized", logger.info),
        ("debug", "colorized", logger.warning),
        ("debug", "colorized", logger.error),
        ("debug", "colorized", logger.critical),
        ("debug", "plain", logger.debug),
        ("debug", "plain", logger.info),
        ("debug", "plain", logger.warning),
        ("debug", "plain", logger.error),
        ("debug", "plain", logger.critical),
    ],
)
def test_all_formatters_work_correctly(ll_env, lf_env, func):
    """
    We could unit test the formatters individually, but to ensure we capture any edge cases which
    may occur due to conditional logic based on log level or other configurations, we instead run
    the logger configuration the way it normally would be run and then we invoke the global log
    methods.
    """
    os.environ["LOG_LEVEL"] = ll_env
    os.environ["LOG_FORMATTER"] = lf_env
    ConfigureLogger().run()
    func("test message")

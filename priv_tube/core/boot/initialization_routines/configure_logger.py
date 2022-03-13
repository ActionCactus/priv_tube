from priv_tube.core.boot.initialization_routines.initialization_routine import InitializationRoutine
from priv_tube.core.boot.initialization_routines.execution_targets import ExecutionTargets
from priv_tube.core.exceptions import SystemConfigurationError
from time import asctime, localtime
from typing import Tuple
import logging
import os

logger = logging.getLogger(__name__)


class ConfigureLogger(InitializationRoutine):
    """
    Configures logging for the entire project.
    """

    # Log level resolution names
    LVL_RES_APP_DEFAULT = "DEFAULT"
    LVL_RES_ENV_VARIABLE = "ENV"
    # Formatter resolution names
    FMT_RES_APP_DEFAULT = "DEFAULT"
    FMT_RES_ENV_VARIABLE = "ENV"

    # Maps log level strings which can be specified by the user to actual log levels
    _log_level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    @property
    def name(self) -> str:
        return "Configure Logger"

    def run(self):
        # Resolve admin configuration
        default_log_level, ll_name, ll_resolution = self.resolve_default_log_level()
        formatter, f_name, f_resolution = self.resolve_formatter()

        # Configure the stream handler the logger will use
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        # Set globals
        logger.addHandler(handler)
        logger.setLevel(default_log_level)

        # Log results
        logger.debug(f"Log level set to {ll_name} by {ll_resolution}.  Formatter set to {f_name} by {f_resolution}.")

    @property
    def execution_target(self) -> ExecutionTargets:
        return ExecutionTargets.PRE_SYSTEM_CHECK

    def resolve_default_log_level(self) -> Tuple[int, str, str]:
        """
        Order of resolution (highest levels overruled by lowest levels):
            - LOG_LEVEL environment variable
            - Hardcoded default
        """
        environment_variable = os.environ.get("LOG_LEVEL", None)

        level = logging.DEBUG
        resolution = ""
        if not environment_variable:
            resolution = ConfigureLogger.LVL_RES_APP_DEFAULT
        else:
            uc_environment_variable = environment_variable.upper()
            specified_level = ConfigureLogger._log_level_map.get(uc_environment_variable, None)
            if not specified_level:
                # The admin has specified an invalid log level
                raise SystemConfigurationError(
                    f"Log level {environment_variable} is invalid.  Select from the following: "
                    + str(ConfigureLogger._log_level_map.keys())
                )
            resolution = ConfigureLogger.LVL_RES_ENV_VARIABLE

        return (level, logging.getLevelName(level), resolution)

    def resolve_formatter(self) -> Tuple[logging.Formatter, str, str]:
        """
        Order of resolution (highest levels overruled by lowest levels):
            - LOG_FORMATTER environment variable
            - Hardcoded default
        """
        environment_variable = os.environ.get("LOG_FORMATTER", None)

        if not environment_variable:
            return (ColorizedLogFormatter(), "COLORIZED", ConfigureLogger.FMT_RES_APP_DEFAULT)
        else:
            uc_environment_variable = environment_variable.upper()
            specified_formatter = _log_formatter_map.get(uc_environment_variable, None)
            if not specified_formatter:
                # The admin has specified a formatter which doesn't exist
                raise SystemConfigurationError(
                    f"Log formatter {environment_variable} is invalid.  Select from the following: "
                    + str(_log_formatter_map.keys())
                )
            return (specified_formatter(), environment_variable, ConfigureLogger.FMT_RES_ENV_VARIABLE)


class PlainTextLogFormatter(logging.Formatter):
    """
    A log formatter with no colors which prepends a timestamp and a log level to every message.
    """

    _shortened_level_map = {logging.WARNING: "WARN", logging.CRITICAL: "CRTCL"}

    def format(self, record: logging.LogRecord) -> str:
        trimmed_level = ColorizedLogFormatter._shortened_level_map.get(record.levelno, record.levelname)
        formatted_level = trimmed_level.ljust(6, " ")

        # Reference LogRecord.msg instead of LogRecord.message because the former is what is set by default
        return "[{0}][ {1}] {2}".format(asctime(localtime(record.created)), formatted_level, record.msg)


class ColorizedLogFormatter(logging.Formatter):
    """
    A colored log formatter which prepends a timestamp and a log level to every message.
    """

    _shortened_level_map = {logging.WARNING: "WARN", logging.CRITICAL: "CRTCL"}
    _color_map = {
        logging.DEBUG: "\033[0;36m",
        logging.INFO: "\033[0;32m",
        logging.WARN: "\033[0;33m",
        logging.WARNING: "\033[0;33m",
        logging.ERROR: "\033[0;31m",
        logging.CRITICAL: "\033[1;91m",
    }

    def format(self, record: logging.LogRecord) -> str:
        trimmed_level = ColorizedLogFormatter._shortened_level_map.get(record.levelno, record.levelname)
        formatted_level = trimmed_level.ljust(6, " ")
        colored_level = ColorizedLogFormatter._color_map.get(record.levelno, "\033[0;33m") + formatted_level + "\033[0m"

        # Reference LogRecord.msg instead of LogRecord.message because the former is what is set by default
        return "[{0}][ {1}] {2}".format(asctime(localtime(record.created)), colored_level, record.msg)


# Maps the LOG_FORMATTER env variable to a formatter
_log_formatter_map = {"COLORIZED": ColorizedLogFormatter, "PLAIN": PlainTextLogFormatter}

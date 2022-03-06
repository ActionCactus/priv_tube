import logging

from abc import ABC, abstractmethod
from typing import List

from priv_tube.core.boot.initialization_routines.execution_targets import ExecutionTargets

# from priv_tube.core.boot.initialization_routines.configure_logger import ConfigureLogger
# from priv_tube.core.boot.initialization_routines.display_sysadmin_welcome_message import DisplaySysadminWelcomeMessage
# from priv_tube.core.boot.initialization_routines.prompt_sysadmin_on_first_boot import PromptSysadminOnFirstBoot


class InitializationRoutine(ABC):
    """
    A routine to be performed on application boot.  Can be used for things like setting up configurations and globals,
    printing a welcome message to system admins, etc.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def run(self):
        pass

    @property
    @abstractmethod
    def execution_target(self) -> ExecutionTargets:
        pass

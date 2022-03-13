import logging

from abc import ABC, abstractmethod
from typing import List

from priv_tube.core.boot.initialization_routines.execution_targets import ExecutionTargets


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
        """
        The point in the initialization process at which this Routine will be executed.
        """
        pass

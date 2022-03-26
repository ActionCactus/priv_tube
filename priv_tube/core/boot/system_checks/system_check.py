from abc import ABC, abstractmethod


class SystemCheck(ABC):
    """
    A check to be performed on app initialization.  Used for things like connectivity checks for required external
    services, configuration validation, etc.  Any error output here is intended to be presented to the system
    administrator booting up the application.
    """

    def run(self):
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def is_required(self) -> bool:
        pass

    @abstractmethod
    def perform(self):
        pass

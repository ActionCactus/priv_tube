import logging
from priv_tube.core.boot.initialization_routines.execution_targets import ExecutionTargets
from priv_tube.core.boot.initialization_routines.initialization_routine import InitializationRoutine

logger = logging.getLogger(__name__)

class DisplaySysadminWelcomeMessage(InitializationRoutine):
    @property
    def name(self) -> str:
        return "Display System Administrator Welcome Message"

    def run(self):
        logger.info("System setup complete.  Enjoy your media!")

    @property
    def execution_target(self) -> ExecutionTargets:
        return ExecutionTargets.POST_SYSTEM_CHECK

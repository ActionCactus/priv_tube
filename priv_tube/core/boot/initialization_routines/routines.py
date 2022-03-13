import logging
import sys

from typing import List
from priv_tube.core.boot.initialization_routines.execution_targets import ExecutionTargets
from priv_tube.core.boot.initialization_routines.configure_logger import ConfigureLogger
from priv_tube.core.boot.initialization_routines.display_sysadmin_welcome_message import DisplaySysadminWelcomeMessage
from priv_tube.core.boot.initialization_routines.initialization_routine import InitializationRoutine
from priv_tube.core.boot.initialization_routines.prompt_sysadmin_on_first_boot import PromptSysadminOnFirstBoot


logger = logging.getLogger(__name__)


class RoutineFactory:
    routines: List[InitializationRoutine] = [
        ConfigureLogger(),
        PromptSysadminOnFirstBoot(),
        DisplaySysadminWelcomeMessage(),
    ]

    def get_routines_for_target_stage(self, stage: ExecutionTargets) -> List[InitializationRoutine]:
        retval = []
        for routine in self.routines:
            if routine.execution_target != stage:
                continue
            retval.append(routine)

        return retval


default_factory = RoutineFactory()


def initialize(stage: ExecutionTargets, factory: RoutineFactory = None):
    """
    Runs all initialization routines for the specified stage.  Shuts down the application if an error occurs.
    """
    if not factory:
        factory = default_factory

    try:
        for routine in factory.get_routines_for_target_stage(stage):
            logger.debug(f"Beginning init routine {routine.name}")
            routine.run()
    except Exception as e:
        logger.critical(
            f"An error occurred while initializing during step '{routine.name}' - shutting down.", exc_info=e
        )
        sys.exit(1)

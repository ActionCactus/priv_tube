from priv_tube.core.boot.initialization_routines.execution_targets import ExecutionTargets
from priv_tube.core.boot.initialization_routines.initialization_routine import InitializationRoutine
from priv_tube.database.repositories.system_flags import SystemFlags


class PromptSysadminOnFirstBoot(InitializationRoutine):
    """
    Creates a blocking user prompt which prevents Flask from booting up the web app until the system
    administrator performs the required environment setup steps.  This is done to ensure various
    required system configurations which don't ship with the freshly built image, like a Keycloak
    database, are completed before the application is run.
    """

    @property
    def name(self) -> str:
        return "Prompt System Administrator For Setup"

    def run(self):
        if SystemFlags.is_enabled("system_setup_complete"):
            return

        self._prompt_user()
        SystemFlags.enable("system_setup_complete")


    @property
    def execution_target(self) -> ExecutionTargets:
        return ExecutionTargets.PRE_SYSTEM_CHECK

    def _prompt_user(self):
        input("Set up your environment now (press ENTER when complete).")

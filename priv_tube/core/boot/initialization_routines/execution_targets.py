from enum import Enum


class ExecutionTargets(Enum):
    # Run the initialization routine before system health checks are performed
    PRE_SYSTEM_CHECK = 1
    # Run the initialization routine after system health checks are performed
    POST_SYSTEM_CHECK = 2

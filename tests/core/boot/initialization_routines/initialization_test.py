from unittest import TestCase

import pytest
from priv_tube.core.boot.initialization_routines.execution_targets import ExecutionTargets
from priv_tube.core.boot.initialization_routines.initialization_routine import InitializationRoutine
from priv_tube.core.boot.initialization_routines.routines import RoutineFactory, initialize, default_factory
from unittest.mock import Mock

from priv_tube.core.exceptions import SystemConfigurationError


class InitializationTest(TestCase):
    def test_get_routines_on_factory_doesnt_have_errors_if_no_routines_are_declared(self):
        factory = RoutineFactory()
        factory.routines = []
        assert factory.get_routines_for_target_stage(ExecutionTargets.PRE_SYSTEM_CHECK) == []

    def test_get_routines_filters_out_irrelevant_routines(self):
        pre_routine = Mock(spec=InitializationRoutine)
        pre_routine.execution_target = ExecutionTargets.PRE_SYSTEM_CHECK

        post_routine = Mock(spec=InitializationRoutine)
        post_routine.execution_target = ExecutionTargets.POST_SYSTEM_CHECK

        factory = RoutineFactory()
        factory.routines = [pre_routine, post_routine]

        results = factory.get_routines_for_target_stage(ExecutionTargets.PRE_SYSTEM_CHECK)

        assert len(results) == 1
        assert results[0].execution_target == ExecutionTargets.PRE_SYSTEM_CHECK

    def test_initialize_runs_routines_in_specified_stage(self):
        routine_a = Mock(spec=InitializationRoutine)
        routine_a.run = Mock()
        routine_a.execution_target = ExecutionTargets.PRE_SYSTEM_CHECK

        routine_b = Mock(spec=InitializationRoutine)
        routine_b.run = Mock()
        routine_b.execution_target = ExecutionTargets.POST_SYSTEM_CHECK

        factory = RoutineFactory()
        factory.routines = [routine_a, routine_b]

        initialize(ExecutionTargets.PRE_SYSTEM_CHECK, factory)

        routine_a.run.assert_called_once()
        routine_b.run.assert_not_called()

    def test_initialize_gracefully_exits_application_on_error(self):
        routine_a = Mock(spec=InitializationRoutine)
        routine_a.run = Mock(side_effect=SystemConfigurationError("Some random error"))
        routine_a.execution_target = ExecutionTargets.PRE_SYSTEM_CHECK

        factory = RoutineFactory()
        factory.routines = [routine_a]

        with self.assertRaises(SystemExit):
            initialize(ExecutionTargets.PRE_SYSTEM_CHECK, factory)


@pytest.mark.parametrize("target", [(ExecutionTargets.PRE_SYSTEM_CHECK), (ExecutionTargets.POST_SYSTEM_CHECK)])
def test_default_factory_can_get_routines_for_each_stage_without_error(target: ExecutionTargets):
    default_factory.get_routines_for_target_stage(target)

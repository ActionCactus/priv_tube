from priv_tube.core.boot.initialization_routines.prompt_sysadmin_on_first_boot import PromptSysadminOnFirstBoot
from unittest.mock import DEFAULT, Mock, patch


def test_system_setup_complete_results_in_continuation():
    with patch.multiple(
        "priv_tube.database.repositories.system_flags.SystemFlags", is_enabled=Mock(return_value=True), enable=DEFAULT
    ) as stubs:
        enable_stub: Mock = stubs.get("enable")
        PromptSysadminOnFirstBoot().run()
        enable_stub.assert_not_called()


def test_system_setup_incomplete_prompts_user_input():
    with patch.multiple(
        "priv_tube.database.repositories.system_flags.SystemFlags",
        is_enabled=Mock(return_value=False),
        enable=DEFAULT,
    ) as stubs:
        enable_stub: Mock = stubs.get("enable")
        routine = PromptSysadminOnFirstBoot()
        routine._prompt_user = Mock()
        routine.run()
        routine._prompt_user.assert_called_once()
        enable_stub.assert_called_once()

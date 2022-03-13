from unittest import TestCase

from priv_tube.core.boot.initialization_routines.display_sysadmin_welcome_message import DisplaySysadminWelcomeMessage


class DisplaySysadminWelcomeMessageTest(TestCase):
    """
    V1 is just a log call - wrote a test to assert no errors occur when running
    all of the defined methods.
    """

    def test_running_doesnt_result_in_errors(self):
        instance = DisplaySysadminWelcomeMessage()
        assert instance.execution_target
        assert instance.name
        instance.run()

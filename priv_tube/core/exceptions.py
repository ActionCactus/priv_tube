class SystemConfigurationError(Exception):
    """
    An exception indicating the system is misconfigured.  Every SystemConfigurationError should be a clear message to the system
    administrator that they need to change something in their deployment.
    """

    pass

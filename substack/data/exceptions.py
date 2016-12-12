from substack.data.logger import logger


class SubStackException(Exception):
    """
    A small class that defines a BaseFrameworkException.
    """

    def __init__(self, message):
        self.value = str(message)
        Exception.__init__(self, self.value)
        logger.exception(self.value)

    def __str__(self):
        return self.value


class PluginException(SubStackException):
    pass


class ProfileException(SubStackException):
    pass


class RequesterException(SubStackException):
    pass

import logging
from substack.helper.utils import LOG_PATH


class Logger:
    """
    This class is based on logging class, it's logging the entire process of the main program
    """

    def __init__(self):
        self.logger = logging.getLogger("SubStack")
        self.set_up()

    def set_up(self):
        file_handler = logging.FileHandler(LOG_PATH)
        stream_handler = logging.StreamHandler()
        handlers = [file_handler, stream_handler]
        formatter = logging.Formatter('[%(levelname)5s] %(asctime)s  %(message)s')

        self.logger.setLevel(logging.INFO)

        for handler in handlers:
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def error(self, msg):
        self.logger.error(msg)

    def exception(self, msg):
        self.logger.exception(msg)


logger = Logger()

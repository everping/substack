import logging
from config import config


class Logger:
    """
    This class is based on logging class, it's logging the entire process of the main program
    """

    def __init__(self):
        self.active = config.load("logger")['active']
        self.log_path = config.load("logger")['path']
        self.logger = logging.getLogger("SubStack")
        self.set_up()

    def set_up(self):
        file_handler = logging.FileHandler(self.log_path)
        stream_handler = logging.StreamHandler()
        handlers = [file_handler, stream_handler]
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s  %(message)s')

        self.logger.setLevel(logging.INFO)

        for handler in handlers:
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, msg):
        if self.active:
            self.logger.info(msg)

    def warning(self, msg):
        if self.active:
            self.logger.warning(msg)

    def debug(self, msg):
        if self.active:
            self.logger.debug(msg)

    def error(self, msg):
        if self.active:
            self.logger.error(msg)


logger = Logger()

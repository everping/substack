import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()

logger.addHandler(ch)

logger.info("hello")
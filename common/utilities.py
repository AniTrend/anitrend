import logging
from logging import Logger
from .helpers import Logging


class LoggingUtility:

    def __init__(self, log_level: str) -> None:
        super().__init__()
        self.__log_level = log_level

    def get_default_logger(self, name: str) -> Logger:
        logging.setLoggerClass(Logging)
        logger = logging.getLogger(name)
        logger.setLevel(self.__log_level)
        return logger

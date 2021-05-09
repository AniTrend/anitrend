import logging
from urllib.parse import urlparse
from logging import Logger
from typing import Union, Optional, List

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


class RegexUtility:

    @staticmethod
    def extract_id_if_matches(urls: List[str], domain_name: str) -> Optional[str]:
        for url in urls:
            url_parse = urlparse(url)
            if url_parse.hostname == domain_name:
                return url_parse.path.split("/")[-1]
        return None

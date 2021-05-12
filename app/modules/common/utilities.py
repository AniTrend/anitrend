import logging
from urllib.parse import urlparse
from logging import Logger
from typing import Optional, List

from .helpers import Logging


class LoggingUtility:

    def __init__(self, is_debug: bool) -> None:
        super().__init__()
        cut_off_log_level = "DEBUG"
        if not is_debug:
            cut_off_log_level = "INFO"
        self.__log_level = cut_off_log_level

    def get_default_logger(self, name: str) -> Logger:
        logging.setLoggerClass(Logging)
        logger = logging.getLogger(name)
        logger.setLevel(self.__log_level)
        return logger


class LinkUtility:

    @staticmethod
    def extract_id_if_matches(urls: List[str], domain_name: str) -> Optional[str]:
        for url in urls:
            url_parse = urlparse(url)
            if url_parse.hostname == domain_name:
                return url_parse.path.split("/")[-1]
        return None

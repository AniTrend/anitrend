from abc import ABC
from logging import Logger
from typing import Any, Optional

from uplink import Consumer


class CommonRepository(ABC):
    _logger: Logger

    def __init__(self, logger: Logger) -> None:
        super().__init__()
        self._logger = logger


class DataRepository(CommonRepository):

    def __init__(self, logger: Logger, remote_source: Consumer) -> None:
        super().__init__(logger)
        self._remote_source = remote_source

    def invoke(self, **kwargs) -> Optional[Any]:
        """
        Requests data from a remote source
        :return: Optional payload
        """
        pass

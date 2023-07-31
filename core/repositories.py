import logging
from abc import ABC
from logging import Logger
from typing import Any, Optional

from uplink import Consumer


class RepositoryMixin(ABC):
    _logger: Logger = logging.getLogger('django')


class DataRepository(RepositoryMixin):

    def __init__(self, remote_source: Consumer) -> None:
        self._remote_source = remote_source

    def invoke(self, **kwargs) -> Optional[Any]:
        """
        Requests data from a remote source
        :return: Optional payload
        """
        pass

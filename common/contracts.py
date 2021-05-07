from abc import ABC
from logging import Logger
from django.db.models import Manager


class CommonRepository(ABC):
    _logger: Logger
    _local_source: Manager

    def __init__(self, logger: Logger) -> None:
        super().__init__()
        self._logger = logger

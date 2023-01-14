from abc import ABC
from logging import Logger

from .repositories import DataRepository


class CommonUseCase(ABC):
    _logger: Logger
    _repository: DataRepository

    def __init__(self, repository: DataRepository, logger: Logger) -> None:
        super().__init__()
        self._logger = logger
        self._repository = repository

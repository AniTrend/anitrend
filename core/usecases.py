import logging
from abc import ABC
from logging import Logger

from .repositories import DataRepository


class CommonUseCase(ABC):
    _repository: DataRepository
    _logger: Logger = logging.getLogger('django')

    def __init__(self, repository: DataRepository) -> None:
        super().__init__()
        self._repository = repository

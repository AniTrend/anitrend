from abc import ABC
from logging import Logger
from typing import Any, Optional

from django.utils.datetime_safe import datetime

from data.model_entities import RelationContainerEntity, XemContainerEntity
from data.repositories import XemRepository, RelationRepository, IRepository


class IUseCase(ABC):

    def __init__(self, logger: Logger, repository: IRepository) -> None:
        self._logger = logger
        self._repository = repository

    def _on_post_data_fetched(self, data: Optional[Any]):
        pass


class XemUseCase(IUseCase):
    _repository: XemRepository

    def __init__(self, logger: Logger, repository: XemRepository) -> None:
        super().__init__(logger, repository)

    def _on_post_data_fetched(self, data: Optional[XemContainerEntity]):
        self._logger.debug(f"Fetched data -> {data}")

    def fetch_all_mappings(self, time_frame: datetime):
        data = self._repository.invoke()
        self._on_post_data_fetched(data)


class RelationUseCase(IUseCase):
    _repository: RelationRepository

    def __init__(self, logger: Logger, repository: RelationRepository) -> None:
        super().__init__(logger, repository)

    def _on_post_data_fetched(self, data: Optional[RelationContainerEntity]):
        self._logger.debug(f"Fetched data -> {data}")

    def fetch_all_records(self, time_frame: datetime):
        data = self._repository.invoke()
        self._on_post_data_fetched(data)

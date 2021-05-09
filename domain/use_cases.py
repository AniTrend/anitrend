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
        self._logger.debug(f"Data received for xem -> {data}")
        try:
            if data is not None:
                if data.result == "success":
                    self._repository.map_and_save_results(data)
                else:
                    self._logger.warning(f"Data result status is not `success` possible reason: {data.message}")
            else:
                raise RuntimeError(f"Data received for relations was null")
        except Exception as e:
            self._logger.error(f"Unable to complete execution", exc_info=e)
            raise e

    def fetch_all_mappings(self, time_frame: datetime):
        try:
            data = self._repository.invoke()
            self._on_post_data_fetched(data)
        except Exception as e:
            self._logger.error(f"Uncaught exception", exc_info=e)
            raise e


class RelationUseCase(IUseCase):
    _repository: RelationRepository

    def __init__(self, logger: Logger, repository: RelationRepository) -> None:
        super().__init__(logger, repository)

    def _on_post_data_fetched(self, data: Optional[RelationContainerEntity]):
        try:
            self._logger.debug(f"Data received for relations -> {data}")
            if data is not None:
                self._repository.map_and_save_results(data)
            else:
                raise RuntimeError(f"Data received for relation was null")
        except Exception as e:
            self._logger.error(f"Unable to complete execution", exc_info=e)
            raise e

    def fetch_all_records(self, time_frame: datetime):
        try:
            data = self._repository.invoke()
            self._on_post_data_fetched(data)
        except Exception as e:
            self._logger.error(f"Uncaught exception", exc_info=e)
            raise e


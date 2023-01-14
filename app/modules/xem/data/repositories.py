from json import JSONDecodeError
from logging import Logger
from typing import Optional, Any

from mongoengine import QuerySetManager
from uplink import Consumer

from core.errors import NoDataError
from core.repositories import DataRepository

from ..domain.entities import XemContainer
from ..models import Xem
from .sources import RemoteSource


class Repository(DataRepository):
    _remote_source: RemoteSource

    def __init__(self, logger: Logger, remote_source: Consumer) -> None:
        super().__init__(logger, remote_source)
        self.__xem: QuerySetManager = Xem.objects

    def map_and_save_results(self, container: XemContainer) -> Any:
        changed_records: int = 0
        self._logger.info(f"Mapping and save results starting")
        for _id, _titles in container.data.items():
            _xem = self.__xem.modify(
                upsert=True,
                id=_id,
                titles=_titles
            )
            if _xem:
                changed_records += 1
                self._logger.info(f"Added/Updated entry -> {_xem.id}")

        return {
            "changed": changed_records
        }

    def __on_result(self, data: XemContainer):
        if data is not None:
            if data.result == "success":
                return self.map_and_save_results(data)
            else:
                self._logger.warning(f"Data result status is not `success` possible reason: {data.message}")
                raise NoDataError(data.message)
        else:
            raise NoDataError(f"Data received for relations was null")

    def invoke(self, **kwargs) -> Optional[Any]:
        try:
            result = self._remote_source.get_all_names(
                origin="tvdb",
                language="all",
                default_names=1
            )
            return self.__on_result(result)
        except JSONDecodeError as e:
            self._logger.error(f"Malformed response with error message `{e.doc}`", exc_info=e)
            raise e

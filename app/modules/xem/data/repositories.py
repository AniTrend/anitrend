from json import JSONDecodeError
from logging import Logger
from typing import Optional, Any

from django.db.models import QuerySet
from uplink import Consumer

from app.modules.common.errors import NoDataError
from app.modules.common.repositories import DataRepository

from ..domain.entities import XemContainer
from ..models import Xem
from .sources import RemoteSource


class Repository(DataRepository):
    _remote_source: RemoteSource

    def __init__(self, logger: Logger, remote_source: Consumer) -> None:
        super().__init__(logger, remote_source)
        self.__xem: QuerySet = Xem.objects

    def map_and_save_results(self, container: XemContainer) -> Any:
        created_records: int = 0
        updated_records: int = 0
        self._logger.info(f"Mapping and save results starting")
        for _id, _titles in container.data.items():
            _xem, created = self.__xem.update_or_create(
                id=_id,
                titles=_titles
            )
            if created:
                created_records += 1
                self._logger.info(f"Added new entry -> {_xem.id}")
            else:
                updated_records += 1
                self._logger.info(f"Updated entry -> {_xem.id}")

        return {
            "created": created_records,
            "updated": updated_records
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

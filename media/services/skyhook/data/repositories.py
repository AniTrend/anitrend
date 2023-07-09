from json import JSONDecodeError
from typing import Optional

from uplink import Consumer

from core.repositories import DataRepository
from ..data.sources import RemoteSource
from ..domain.entities import SkyhookShow


class Repository(DataRepository):
    _remote_source: RemoteSource

    def __init__(self, remote_source: Consumer) -> None:
        super().__init__(remote_source)

    def invoke(self, **kwargs) -> Optional[SkyhookShow]:
        try:
            tvdb_id = kwargs.pop("tvdb_id")
            data = self._remote_source.get_show_by_tvdb(tvdb_id=tvdb_id)
            return data
        except JSONDecodeError as e:
            self._logger.error(f"Malformed response with error message `{e.doc}`", exc_info=e)
            raise e

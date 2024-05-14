from json import JSONDecodeError

from uplink import Consumer

from core.repositories import DataRepository
from ..data.sources import RemoteSource
from ..domain.entities import (ConfigurationModel)


class Repository(DataRepository):
    _remote_source: RemoteSource

    def __init__(self, remote_source: Consumer) -> None:
        super().__init__(remote_source)

    def invoke(self, **kwargs) -> ConfigurationModel:
        try:
            headers = kwargs.get('headers')
            data = self._remote_source.get_config(headers)
            return data
        except JSONDecodeError as e:
            self._logger.error(f"Malformed response with error message `{e.doc}`", exc_info=e)
            raise e

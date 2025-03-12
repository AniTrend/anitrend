from json import JSONDecodeError
from uplink import Consumer
from config.data.schemas import ConfigurationSchema
from core.repositories import DataRepository
from ..data.sources import RemoteSource


class Repository(DataRepository):
    _remote_source: RemoteSource

    def invoke(self, **kwargs) -> ConfigurationSchema:
        try:
            headers = kwargs.get("headers")
            data = self._remote_source.get_config(headers=headers)
            return data
        except JSONDecodeError as e:
            self._logger.error(
                f"Malformed response with error message `{e.doc}`", exc_info=e
            )
            raise e

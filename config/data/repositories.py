from json import JSONDecodeError
from typing import Optional, Any

from uplink import Consumer

from core.errors import NoDataError
from core.repositories import DataRepository
from .schemas import ConfigurationSchema
from ..data.sources import RemoteSource
from ..domain.entities import (ConfigurationModel, SettingsModel, ImageModel, NavigationModel,
                               NavigationGroupModel, GenreModel)
from pyxtension.streams import stream


class Repository(DataRepository):
    _remote_source: RemoteSource

    def __init__(self, remote_source: Consumer) -> None:
        super().__init__(remote_source)

    def invoke(self, **kwargs) -> ConfigurationModel:
        try:
            data = self._remote_source.get_config()
            return data
        except JSONDecodeError as e:
            self._logger.error(f"Malformed response with error message `{e.doc}`", exc_info=e)
            raise e

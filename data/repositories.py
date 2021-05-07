from json import JSONDecodeError
from logging import Logger
from typing import Optional, Any, List, Dict

from uplink import Consumer
from api.models import Series
from service.models import Mapping
from common.contracts import CommonRepository
from data.remote_sources import XemRemoteSource, RelationRemoteSource
from data.model_entities import RelationContainerEntity, XemContainerEntity


class IRepository(CommonRepository):

    def __init__(self, logger: Logger, remote_source: Consumer) -> None:
        super().__init__(logger)
        self._remote_source = remote_source

    def save(self, items: List[Any]):
        """
        Save a number of items
        :param items: Collection of items to save
        :return:
        """
        pass

    def invoke(self) -> Optional[List]:
        """
        Requests data from a remote source
        :return: Optional items
        """
        pass


class XemRepository(IRepository):
    _remote_source: XemRemoteSource

    def __init__(self, logger: Logger, remote_source: Consumer) -> None:
        super().__init__(logger, remote_source)
        self._local_source = Mapping.objects

    def save(self, items: List[Mapping]):
        self._logger.debug(f"Saving {len(items)} mapping items")
        self._local_source.bulk_create(items)
        self._logger.debug(f"Bulk create completed successfully")

    def map_results(self, items: List[Dict]) -> List[Mapping]:
        pass

    def invoke(self) -> Optional[XemContainerEntity]:
        try:
            result = self._remote_source.get_all_names(
                origin="tvdb",
                language="all",
                default_names=1
            )
            return result
        except self._remote_source.exceptions.ConnectionError as e:
            self._logger.warning("Connection error occurred", exc_info=e)
        except self._remote_source.exceptions.InvalidURL as e:
            self._logger.warning("The supplied url maybe invalid", exc_info=e)
        except self._remote_source.exceptions.ServerTimeout | \
                self._remote_source.exceptions.ConnectionTimeout as e:
            self._logger.warning("Server or connection timeout occurred", exc_info=e)
        except self._remote_source.exceptions.SSLError as e:
            self._logger.warning("Secure socket error occurred", exc_info=e)
        except JSONDecodeError as e:
            self._logger.error(f"Malformed response: {e.doc}", exc_info=e)

        return None


class RelationRepository(IRepository):
    _remote_source: RelationRemoteSource

    def __init__(self, logger: Logger, remote_source: Consumer) -> None:
        super().__init__(logger, remote_source)
        self._local_source = Series.objects

    def save(self, items: List[Series]):
        self._logger.debug(f"Saving {len(items)} relation items")
        self._local_source.bulk_create(items)
        self._logger.debug(f"Bulk create completed successfully")

    def map_results(self, items: List[Any]) -> List[Series]:
        pass

    def invoke(self) -> Optional[RelationContainerEntity]:
        try:
            result = self._remote_source.get_anime_entries()
            return result
        except self._remote_source.exceptions.ConnectionError as e:
            self._logger.warning("Connection error occurred", exc_info=e)
        except self._remote_source.exceptions.InvalidURL as e:
            self._logger.warning("The supplied url maybe invalid", exc_info=e)
        except self._remote_source.exceptions.ServerTimeout | \
                self._remote_source.exceptions.ConnectionTimeout as e:
            self._logger.warning("Server or connection timeout occurred", exc_info=e)
        except self._remote_source.exceptions.SSLError as e:
            self._logger.warning("Secure socket error occurred", exc_info=e)
        except JSONDecodeError as e:
            self._logger.error(f"Malformed response: {e.doc}", exc_info=e)

        return None

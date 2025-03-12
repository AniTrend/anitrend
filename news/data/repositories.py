from typing import Optional, Dict

from uplink import Consumer

from core.repositories import DataRepository
from news.data.schemas import NewsConnectionSchema
from ..data.sources import RemoteSource


class NewsRepository(DataRepository):
    _remote_source: RemoteSource

    def invoke(self, **kwargs) -> NewsConnectionSchema:
        """Fetch paginated news using cursor-based pagination
        :param headers: Request headers
        :param after: Cursor for next page
        :param before: Cursor for previous page
        :param limit: Limit of records to fetch
        :return: NewsConnectionSchema object
        """
        try:
            data = self._remote_source.get_news(
                headers=kwargs.get("headers"),
                after=kwargs.get("after"),
                before=kwargs.get("before"),
                limit=kwargs.get("limit"),
            )
            return data
        except Exception as e:
            self._logger.error(f"Failed to fetch news", exc_info=e)
            raise e

from typing import Dict, List, Optional

from marshmallow import EXCLUDE
from marshmallow_dataclass import class_schema

from core.repositories import DataRepository
from news.data.schemas import NewsConnectionSchema, NewsSchema
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

    def fetch_feed(
        self, *, headers: Dict[str, str], locale: Optional[str]
    ) -> List[NewsSchema]:
        try:
            raw_feed = self._remote_source.get_news_feed(headers=headers, locale=locale)
            schema = class_schema(NewsSchema)()
            return schema.load(raw_feed, many=True, unknown=EXCLUDE)
        except Exception as e:
            self._logger.error("Failed to fetch news feed", exc_info=e)
            raise e

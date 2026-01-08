from typing import Optional, Dict, List

from core.usecases import CommonUseCase
from news.data.schemas import NewsConnectionSchema, NewsSchema


class NewsUseCase(CommonUseCase):
    def fetch_news_connection(
        self,
        headers: Dict[str, str],
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Optional[NewsConnectionSchema]:
        """Fetch paginated news using cursor-based pagination
        :param headers: Request headers
        :param after: Cursor for next page
        :param before: Cursor for previous page
        :return: NewsConnectionSchema object
        """
        try:
            data = self._repository.invoke(
                headers=headers,
                after=after,
                before=before,
                limit=limit,
            )
            return data
        except Exception as e:
            self._logger.error(f"Failed to fetch news", exc_info=e)
            raise e

    def fetch_news_feed(
        self, headers: Dict[str, str], locale: Optional[str] = None
    ) -> Optional[List[NewsSchema]]:
        try:
            return self._repository.fetch_feed(headers=headers, locale=locale)
        except Exception as e:
            self._logger.error("Failed to fetch news feed", exc_info=e)
            raise e

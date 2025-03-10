from typing import Optional, Dict

from core.usecases import CommonUseCase
from .entities import NewsConnectionModel


class NewsUseCase(CommonUseCase):
    def fetch_news_connection(
        self,
        headers: Dict[str, str],
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Optional[NewsConnectionModel]:
        """Fetch paginated news using cursor-based pagination
        :param headers: Request headers
        :param after: Cursor for next page
        :param before: Cursor for previous page
        :return: NewsConnectionModel object
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
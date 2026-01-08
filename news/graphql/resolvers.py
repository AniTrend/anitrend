from typing import List, Optional

from strawberry.types.info import ContextType

from news.di.containers import NewsContainer
from core.utilities import get_forwarded_headers
from .types import News, NewsConnection


def resolve_news_connection(
    context: ContextType,
    after: Optional[str] = None,
    before: Optional[str] = None,
    limit: Optional[int] = None,
    use_case_provider=NewsContainer.use_case,
) -> Optional[NewsConnection]:
    """Resolve news query with cursor-based pagination
    :param context: GraphQL context
    :param after: Cursor for next page
    :param before: Cursor for previous page
    :return: NewsConnection object
    """
    use_case = use_case_provider()
    forwarded_headers = get_forwarded_headers(context)
    result = use_case.fetch_news_connection(
        headers=forwarded_headers,
        after=after,
        before=before,
        limit=limit,
    )
    return NewsConnection.from_model(result) if result else None


def resolve_news_feed(
    context: ContextType,
    locale: Optional[str] = None,
    use_case_provider=NewsContainer.use_case,
) -> List[News]:
    use_case = use_case_provider()
    forwarded_headers = get_forwarded_headers(context)
    feed = use_case.fetch_news_feed(headers=forwarded_headers, locale=locale)
    return [News.from_model(item) for item in feed or []]

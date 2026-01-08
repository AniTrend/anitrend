import strawberry
from typing import Annotated, Optional, List
from strawberry.types import Info

from .resolvers import resolve_news_connection, resolve_news_feed
from .types import NewsConnection, News


@strawberry.type
class NewsQuery:

    @strawberry.field(description="Paginated news items using cursor-based pagination")
    def newsConnection(
        self,
        info: Info,
        after: Optional[
            Annotated[
                str, strawberry.argument(description="The cursor for the next page")
            ]
        ] = None,
        before: Optional[
            Annotated[
                str, strawberry.argument(description="The cursor for the previous page")
            ]
        ] = None,
        limit: Optional[
            Annotated[
                int,
                strawberry.argument(description="The size of the list, default is 10"),
            ]
        ] = None,
    ) -> Optional[NewsConnection]:
        try:
            return resolve_news_connection(
                context=info.context, after=after, before=before, limit=limit
            )
        except Exception as e:
            raise Exception(f"An error occurred while fetching news")

    @strawberry.field(description="Localized news feed")
    def newsFeed(
        self,
        info: Info,
        locale: Optional[
            Annotated[str, strawberry.argument(description="Locale code, e.g. en-US")]
        ] = None,
    ) -> List[News]:
        return resolve_news_feed(context=info.context, locale=locale)

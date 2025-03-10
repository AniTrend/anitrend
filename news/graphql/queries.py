import strawberry
from typing import Annotated, Optional
from strawberry.types import Info

from .resolvers import resolve_news
from .types import NewsConnection


@strawberry.type
class NewsQuery:

    @strawberry.field(description="Paginated news items using cursor-based pagination")
    def newsConnection(
        self, 
        info: Info,
        after: Annotated[Optional[str], strawberry.argument(description="The cursor for the next page")],
        before: Annotated[Optional[str], strawberry.argument(description="The cursor for the previous page")],
        limit: Annotated[Optional[int], strawberry.argument(description="The size of the list, default is 10")],
    ) -> Optional[NewsConnection]:
        try:
            return resolve_news(
                context=info.context,
                after=after,
                before=before,
                limit=limit
            )
        except Exception as e:
            raise Exception(f"An error occurred while fetching news")

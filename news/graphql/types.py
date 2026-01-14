import strawberry
from typing import Optional, List


@strawberry.type
class News:
    id: str = strawberry.field(description="Unique identifier")
    title: str = strawberry.field(description="News title")
    description: str = strawberry.field(description="News description/summary")
    content: str = strawberry.field(description="Full news content")
    publishedOn: int = strawberry.field(description="Publishing timestamp")
    link: str = strawberry.field(description="News source URL")
    category: Optional[str] = strawberry.field(description="Category label", default=None)
    genre: Optional[str] = strawberry.field(description="Genre label", default=None)
    area: Optional[str] = strawberry.field(description="Area or region", default=None)
    lang: Optional[str] = strawberry.field(description="Locale code", default=None)
    image: Optional[str] = strawberry.field(description="News thumbnail image URL", default=None)


@strawberry.type
class NewsConnection:
    count: int = strawberry.field(description="Total number of news items")
    first: Optional[str] = strawberry.field(description="First news item ID", default=None)
    last: Optional[str] = strawberry.field(description="Last news item ID", default=None)
    data: List[News] = strawberry.field(description="Paginated news items")

import strawberry
from typing import Optional, List


@strawberry.type
class News:
    id: str = strawberry.field(description="Unique identifier")
    title: str = strawberry.field(description="News title")
    author: str = strawberry.field(description="News author")
    description: str = strawberry.field(description="News description/summary")
    content: str = strawberry.field(description="Full news content")
    image: Optional[str] = strawberry.field(description="News thumbnail image URL")
    publishedOn: int = strawberry.field(description="Publishing timestamp")
    link: str = strawberry.field(description="News source URL")


@strawberry.type
class NewsConnection:
    count: int = strawberry.field(description="Total number of news items")
    first: str = strawberry.field(description="First news item ID")
    last: str = strawberry.field(description="Last news item ID")
    data: List[News] = strawberry.field(description="Paginated news items")

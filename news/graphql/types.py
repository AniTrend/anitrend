import strawberry
from typing import Optional, List

from news.data.schemas import NewsConnectionSchema, NewsSchema


@strawberry.type
class News:
    id: str = strawberry.field(description="Unique identifier")
    title: str = strawberry.field(description="News title")
    description: str = strawberry.field(description="News description/summary")
    content: str = strawberry.field(description="Full news content")
    link: str = strawberry.field(description="News source URL")
    publishedOn: int = strawberry.field(description="Publishing timestamp")
    author: Optional[str] = strawberry.field(description="News author", default=None)
    image: Optional[str] = strawberry.field(
        description="News thumbnail image URL", default=None
    )
    category: Optional[str] = strawberry.field(
        description="News category", default=None
    )
    genre: Optional[str] = strawberry.field(description="News genre", default=None)
    area: Optional[str] = strawberry.field(description="News area", default=None)
    lang: Optional[str] = strawberry.field(description="News language", default=None)

    @classmethod
    def from_model(cls, model: NewsSchema) -> "News":
        return cls(
            id=model.id,
            title=model.title,
            description=model.description,
            content=model.content,
            link=model.link,
            publishedOn=model.publishedOn,
            author=model.author,
            image=model.image,
            category=model.category,
            genre=model.genre,
            area=model.area,
            lang=model.lang,
        )


@strawberry.type
class NewsConnection:
    count: int = strawberry.field(description="Total number of news items")
    data: List[News] = strawberry.field(description="Paginated news items")
    first: Optional[str] = strawberry.field(
        description="First news item ID", default=None
    )
    last: Optional[str] = strawberry.field(
        description="Last news item ID", default=None
    )

    @classmethod
    def from_model(cls, model: NewsConnectionSchema) -> "NewsConnection":
        return cls(
            count=model.count,
            data=[News.from_model(item) for item in model.data],
            first=model.first,
            last=model.last,
        )

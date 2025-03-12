import strawberry


@strawberry.type
class NewsObjectType:
    id: str = strawberry.field(description="News ID")
    title: str = strawberry.field(description="News title")
    image: str = strawberry.field(description="News image URL")
    author: str = strawberry.field(description="News author")
    description: str = strawberry.field(description="News description")
    content: str = strawberry.field(description="News content")
    link: str = strawberry.field(description="News link")
    publishedOn: int = strawberry.field(description="Published timestamp")

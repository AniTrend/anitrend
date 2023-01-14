import graphene


class NewsObjectType(graphene.ObjectType):
    id = graphene.String(
        name="id",
        description="News ID"
    )
    title = graphene.String(
        name="title",
        description="News title"
    )
    image = graphene.String(
        name="image",
        description="News image URL"
    )
    author = graphene.String(
        name="author",
        description="News author"
    )
    description = graphene.String(
        name="description",
        description="News description"
    )
    content = graphene.String(
        name="content",
        description="News content"
    )
    link = graphene.String(
        name="link",
        description="News link"
    )
    publishedOn = graphene.Int(
        name="publishedOn",
        description="Published timestamp"
    )

    class Meta:
        name = "News"
        description = "Industry news and announcements"
        exclude = []

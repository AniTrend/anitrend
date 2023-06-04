import graphene
from graphene import relay, ObjectType


class GenreObjectType(ObjectType):
    genre = graphene.String(
        name="genre",
        description="Genre"
    )
    mediaId = graphene.Int(
        name="mediaId",
        description="Media ID"
    )
    image = graphene.String(
        name="image",
        description="Image banners for relation"
    )

    class Meta:
        name = "Genre"
        description = "Genre and media ID relation"


class HomeObjectType(ObjectType):
    genres = graphene.List(GenreObjectType)

    class Meta:
        name = "Home"
        description = "Home entries"
        interfaces = (relay.Node,)

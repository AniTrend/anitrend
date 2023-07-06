import graphene

from .types import MediaObjectType


class MediaQuery(graphene.ObjectType):
    media = graphene.Field(
        MediaObjectType,
        name="media",
        description="Find a media item by filtering with an id",
        args={
            "id": graphene.ID(required=False, description="Media Id"),
            "tvdb": graphene.Int(required=False, description="TVDB Id"),
            "anidb": graphene.Int(required=False, description="AniDB Id"),
            "anilist": graphene.Int(required=False, description="AniList Id"),
            "animeplanet": graphene.String(required=False, description="AnimePlanet Slug"),
            "notify": graphene.String(required=False, description="Notify.moe Id"),
            "kitsu": graphene.Int(required=False, description="Kitsu Id"),
            "mal": graphene.Int(required=False, description="Mal Id"),
        }
    )

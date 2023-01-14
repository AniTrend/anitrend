from graphene import ID, Int, String, ObjectType, Field

from media.graphql.types import MediaObjectType


class MediaQuery(ObjectType):
    media = Field(
        MediaObjectType,
        name="media",
        description="Find a media item by filtering with an id",
        args={
            "id": ID(required=False, description="Media Id"),
            "tvdb": Int(required=False, description="TVDB Id"),
            "anidb": Int(required=False, description="AniDB Id"),
            "anilist": Int(required=False, description="AniList Id"),
            "animeplanet": String(required=False, description="AnimePlanet Slug"),
            "notify": String(required=False, description="Notify.moe Id"),
            "kitsu": Int(required=False, description="Kitsu Id"),
            "mal": Int(required=False, description="Mal Id"),
        }
    )

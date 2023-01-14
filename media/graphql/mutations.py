from typing import Optional

from graphene import Mutation, InputObjectType, ID, Boolean, Field

from media.graphql.types import MediaObjectType


class MediaInput(InputObjectType):
    id = ID()


class CreateMediaMutation(Mutation):
    class Arguments:
        media_data = MediaInput(required=True)

    media = Field(MediaObjectType)

    @classmethod
    def mutate(cls, info, media_data: Optional[MediaInput] = None):
        return CreateMediaMutation(success=True)

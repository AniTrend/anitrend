from typing import Optional

import graphene

from .types import MediaObjectType


class MediaInput(graphene.InputObjectType):
    id = graphene.ID()


class CreateMediaMutation(graphene.Mutation):
    class Arguments:
        media_data = MediaInput(required=True)

    media = graphene.Field(MediaObjectType)

    @classmethod
    def mutate(cls, info, media_data: Optional[MediaInput] = None):
        return CreateMediaMutation(success=True)

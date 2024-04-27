import graphene
from graphene import ObjectType

from config.graphql.queries import ConfigQuery
from media.graphql.mutations import CreateMediaMutation
from media.graphql.queries import MediaQuery
from media.graphql.types import MediaObjectType


class Mutations(ObjectType):
    create_media = CreateMediaMutation.Field(
        name="createMedia",
        description="Create a media entry"
    )


class Subscriptions(ObjectType):
    pass


class Query(ConfigQuery, MediaQuery, ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations, types=[MediaObjectType])

import graphene
from graphene import ObjectType

from home.graphql.queries import HomeQuery
from config.graphql.queries import ConfigQuery
from media.graphql.queries import MediaQuery
from navigation.graphql.queries import NavigationQuery
from media.graphql.mutations import CreateMediaMutation
from media.graphql.types import MediaObjectType


class Mutations(ObjectType):
    create_media = CreateMediaMutation.Field(
        name="createMedia",
        description="Create a media entry"
    )


class Subscriptions(ObjectType):
    pass


class Query(HomeQuery, ConfigQuery, MediaQuery, NavigationQuery, ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations, types=[MediaObjectType])

import graphene
from graphene import ObjectType

from config.graphql.queries import ConfigQuery
from home.graphql.queries import HomeQuery
from media.graphql.mutations import CreateMediaMutation
from media.graphql.queries import MediaQuery
from media.graphql.types import MediaObjectType
from navigation.graphql.queries import NavigationQuery


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

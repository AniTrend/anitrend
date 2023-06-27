from graphene import ObjectType, Field
from graphql import GraphQLResolveInfo

from .resolvers import resolve_config
from .types import ConfigurationObjectType


class ConfigQuery(ObjectType):
    config = Field(
        ConfigurationObjectType,
        name="config",
        description="Client configuration",
    )

    @staticmethod
    def resolve_config(root, info: GraphQLResolveInfo, **kwargs):
        return resolve_config(info)

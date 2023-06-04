from graphene import ObjectType, Field

from .resolvers import resolve_config
from .types import ConfigurationObjectType
from ..models import Config


class ConfigQuery(ObjectType):
    config = Field(
        ConfigurationObjectType,
        name="config",
        description="Client configuration",
    )

    @staticmethod
    def resolve_config(info, **kwargs):
        return resolve_config(info)

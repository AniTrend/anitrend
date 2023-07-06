from typing import Any
from graphql import GraphQLResolveInfo

from ..models import Config


def resolve_config(info: GraphQLResolveInfo) -> Any:
    """

    :param info:
    :return: Instance of Config
    """
    # enabled_analytics = info.context.feature.isOn("enable-analytics")
    result = Config.objects.get(id=1)
    return result

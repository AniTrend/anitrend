from typing import Any

from ..models import Config


def resolve_config(info) -> Any:
    """

    :param info:
    :return: Instance of Config
    """
    result = Config.objects.get(id=1)
    return result

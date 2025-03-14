from typing import Optional

from strawberry.types.info import ContextType

from config.di.containers import ConfigContainer
from core.utilities import get_forwarded_headers
from .types import Configuration


def resolve_config(
    context: ContextType, use_case_provider=ConfigContainer.use_case
) -> Optional[Configuration]:
    use_case = use_case_provider()
    forwarded_headers = get_forwarded_headers(context)
    result = use_case.fetch_configuration(forwarded_headers)
    return result

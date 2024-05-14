from typing import Optional, Dict

# noinspection PyPackageRequirements
from graphql import GraphQLResolveInfo

from core.utils import get_forwarded_headers
from ..di.containers import UseCaseContainer
from ..domain.entities import ConfigurationModel
from ..domain.usecases import ConfigUseCase


def resolve_config(
        info: GraphQLResolveInfo,
        use_case_provider=UseCaseContainer.use_case
) -> Optional[ConfigurationModel]:
    """
    Configuration resolver
    :param info:
    :param use_case_provider:
    :return: Instance of Config
    """
    use_case: ConfigUseCase = use_case_provider()
    forwarded_headers = get_forwarded_headers(info.context)
    result = use_case.fetch_configuration(forwarded_headers)
    return result

from typing import Optional

# noinspection PyPackageRequirements
from graphql import GraphQLResolveInfo

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
    enabled_analytics = info.context.feature.isOn("enable-analytics")
    result = use_case.fetch_configuration()
    return result

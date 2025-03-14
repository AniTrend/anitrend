import dependency_injector.containers as containers
import dependency_injector.providers as providers
from django.conf import settings

from di import CoreContainer
from ..data.repositories import Repository
from ..data.sources import RemoteSource
from ..domain.usecases import ConfigUseCase


class ConfigContainer(containers.DeclarativeContainer):
    """IoC container of config providers"""

    remote_source = providers.Singleton(
        RemoteSource,
        base_url=settings.ON_THE_EDGE["host"],
        client=CoreContainer.session,
    )

    repository = providers.Singleton(
        Repository,
        remote_source=remote_source,
    )

    use_case = providers.Factory(ConfigUseCase, repository=repository)

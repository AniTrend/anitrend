import dependency_injector.containers as containers
import dependency_injector.providers as providers
from django.conf import settings

from di import CoreContainer
from media.data.repositories import Repository
from media.data.sources import RemoteSource
from media.domain.usecases import MediaUseCase


class MediaContainer(containers.DeclarativeContainer):
    """IoC container of media providers"""

    config = providers.Configuration()

    remote_source = providers.Singleton(
        RemoteSource,
        base_url=settings.ON_THE_EDGE["host"],  # Uses the same endpoint as config
        client=CoreContainer.session,  # Reuses the session from CoreContainer
    )

    repository = providers.Singleton(
        Repository,
        remote_source=remote_source,
    )

    use_case = providers.Factory(
        MediaUseCase,
        repository=repository,
    )

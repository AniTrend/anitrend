import dependency_injector.containers as containers
import dependency_injector.providers as providers
from django.conf import settings

from di import CoreContainer  # Assuming CoreContainer is in the global di module
from ..data.repositories import Repository
from ..data.sources import RemoteSource
from ..domain.usecases import MediaUseCase  # Placeholder for when use cases are defined


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

    # Placeholder for use case provider
    use_case = providers.Factory(
        MediaUseCase,
        repository=repository,
    )

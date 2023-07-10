import dependency_injector.containers as containers
import dependency_injector.providers as providers

from ..data import MediaRepository


class MediaRepositoryContainer(containers.DeclarativeContainer):
    """IoC container of utilities providers."""

    media_repository = providers.Singleton(
        MediaRepository,
    )

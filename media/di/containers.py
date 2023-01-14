import dependency_injector.containers as containers
import dependency_injector.providers as providers

from di import AppContainer
from ..data import MediaRepository


class MediaRepositoryContainer(containers.DeclarativeContainer):
    """IoC container of utilities providers."""
    logging_utility = AppContainer.logging_utility()

    media_repository = providers.Singleton(
        MediaRepository,
        logger=logging_utility.get_default_logger("api.repository"),
    )

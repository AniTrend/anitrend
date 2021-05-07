import dependency_injector.containers as containers
import dependency_injector.providers as providers

from di import MainContainer
from api.repositories import SeriesRepository


class RepositoryProvider(containers.DeclarativeContainer):
    """IoC container of utilities providers."""
    logging_utility = MainContainer.logging_utility()

    series_repository = providers.Singleton(
        SeriesRepository,
        logger=logging_utility.get_default_logger("api.repository"),
    )

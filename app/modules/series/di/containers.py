import dependency_injector.containers as containers
import dependency_injector.providers as providers

from app.dependencies import AppContainer
from ..data import SeriesRepository


class SeriesRepositoryContainer(containers.DeclarativeContainer):
    """IoC container of utilities providers."""
    logging_utility = AppContainer.logging_utility()

    series_repository = providers.Singleton(
        SeriesRepository,
        logger=logging_utility.get_default_logger("api.repository"),
    )

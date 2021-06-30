import dependency_injector.containers as containers
import dependency_injector.providers as providers

from app.dependencies import AppContainer
from ..data.sources import RemoteSource
from ..domain.usecases import SkyhookUseCase
from ..data.repositories import Repository


class RemoteSourceContainer(containers.DeclarativeContainer):
    """IoC container of remote sources providers"""
    remote_source = providers.Singleton(
        RemoteSource,
        base_url="http://skyhook.sonarr.tv/v1/",
        client=AppContainer.session,
    )


class RepositoryContainer(containers.DeclarativeContainer):
    """IoC container of repository providers"""
    __logging_utility = AppContainer.logging_utility()

    repository = providers.Singleton(
        Repository,
        logger=__logging_utility.get_default_logger("service.repository.skyhook"),
        remote_source=RemoteSourceContainer.remote_source(),
    )


class UseCaseContainer(containers.DeclarativeContainer):
    """IoC container for use-cases"""
    __logging_utility = AppContainer.logging_utility()

    use_case = providers.Factory(
        SkyhookUseCase,
        logger=__logging_utility.get_default_logger("service.use_case.skyhook"),
        repository=RepositoryContainer.repository()
    )

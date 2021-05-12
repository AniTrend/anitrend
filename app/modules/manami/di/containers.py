import dependency_injector.containers as containers
import dependency_injector.providers as providers

from app.dependencies import AppContainer
from ..data.sources import RemoteSource
from ..domain.usecases import ManAniUseCase
from ..data.repositories import Repository


class RemoteSourceContainer(containers.DeclarativeContainer):
    """IoC container of remote sources providers"""
    remote_source = providers.Singleton(
        RemoteSource,
        base_url="https://raw.githubusercontent.com/manami-project/anime-offline-database/",
        client=AppContainer.session,
    )


class RepositoryContainer(containers.DeclarativeContainer):
    """IoC container of repository providers"""
    __logging_utility = AppContainer.logging_utility()

    repository = providers.Singleton(
        Repository,
        logger=__logging_utility.get_default_logger("service.repository.manami"),
        remote_source=RemoteSourceContainer.remote_source(),
    )


class UseCaseContainer(containers.DeclarativeContainer):
    """IoC container for use-cases"""
    __logging_utility = AppContainer.logging_utility()

    use_case = providers.Factory(
        ManAniUseCase,
        logger=__logging_utility.get_default_logger("service.use_case.manami"),
        repository=RepositoryContainer.repository()
    )

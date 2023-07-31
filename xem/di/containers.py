import dependency_injector.containers as containers
import dependency_injector.providers as providers

from di import CoreContainer
from ..data.repositories import Repository
from ..data.sources import RemoteSource
from ..domain.usecases import XemUseCase


class RemoteSourceContainer(containers.DeclarativeContainer):
    """IoC container of remote sources providers"""
    remote_source = providers.Singleton(
        RemoteSource,
        base_url="http://thexem.de/",
        client=CoreContainer.session,
    )


class RepositoryContainer(containers.DeclarativeContainer):
    """IoC container of repository providers"""
    repository = providers.Singleton(
        Repository,
        remote_source=RemoteSourceContainer.remote_source(),
    )


class UseCaseContainer(containers.DeclarativeContainer):
    """IoC container for use-cases"""
    use_case = providers.Factory(
        XemUseCase,
        repository=RepositoryContainer.repository()
    )

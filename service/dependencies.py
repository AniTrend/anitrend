import dependency_injector.containers as containers
import dependency_injector.providers as providers
from requests import Session

from di import MainContainer
from data.remote_sources import XemRemoteSource, RelationRemoteSource
from data.repositories import XemRepository, RelationRepository
from domain import XemUseCase, RelationUseCase


class SessionProvider(containers.DeclarativeContainer):
    """IoC container of utilities providers."""
    default_session = providers.Factory(Session)


class RemoteSourceProvider(containers.DeclarativeContainer):
    """IoC container of utilities providers."""
    __client = SessionProvider.default_session()

    from django.conf import settings

    xem_remote_source = providers.Singleton(
        XemRemoteSource,
        base_url=settings.XEM_BASE_URL,
        client=__client,
    )

    relation_remote_source = providers.Singleton(
        RelationRemoteSource,
        base_url=settings.RELATION_BASE_URL,
        client=__client,
    )


class RepositoryProvider(containers.DeclarativeContainer):
    """IoC container of utilities providers."""
    logging_utility = MainContainer.logging_utility()

    xem_repository = providers.Singleton(
        XemRepository,
        logger=logging_utility.get_default_logger("service.repository.xem"),
        remote_source=RemoteSourceProvider.xem_remote_source(),
    )
    relation_repository = providers.Singleton(
        RelationRepository,
        logger=logging_utility.get_default_logger("service.repository.relation"),
        remote_source=RemoteSourceProvider.relation_remote_source(),
    )


class UseCaseProvider(containers.DeclarativeContainer):
    """IoC container of utilities providers."""
    logging_utility = MainContainer.logging_utility()

    xem_use_case = providers.Factory(
        XemUseCase,
        logger=logging_utility.get_default_logger("service.use_case.xem"),
        repository=RepositoryProvider.xem_repository(),
    )
    relation_use_case = providers.Factory(
        RelationUseCase,
        logger=logging_utility.get_default_logger("service.use_case.relation"),
        repository=RepositoryProvider.relation_repository(),
    )

import dependency_injector.containers as containers
import dependency_injector.providers as providers
from uplink.auth import ApiTokenHeader

from app.dependencies import AppContainer
from ..domain.usecases import CrunchyUseCase
from ..data.sources import TokenEndpoint, SigningEndpoint, CmsEndpoint, BucketEndpoint
from ..data.repositories import BucketRepository, CmsRepository, SingingRepository, AuthenticationRepository


class RemoteSourceContainer(containers.DeclarativeContainer):
    """IoC container of remote sources providers"""
    token_source = providers.Singleton(
        TokenEndpoint,
        base_url="https://beta-api.crunchyroll.com/",
        client=AppContainer.session,
        auth=ApiTokenHeader(header="Authorization", token=AppContainer.config.CRUNCHY_TOKEN, prefix="Basic")
    )
    cms_source = providers.Singleton(
        CmsEndpoint,
        base_url="https://beta-api.crunchyroll.com/",
        client=AppContainer.session,
    )
    signing_source = providers.Singleton(
        SigningEndpoint,
        base_url="https://beta-api.crunchyroll.com/",
        client=AppContainer.session,
    )
    bucket_source = providers.Singleton(
        BucketEndpoint,
        base_url="https://beta-api.crunchyroll.com/",
        client=AppContainer.session,
    )


class RepositoryContainer(containers.DeclarativeContainer):
    """IoC container of repository providers"""
    __logging_utility = AppContainer.logging_utility()

    authentication_repository = providers.Singleton(
        AuthenticationRepository,
        logger=__logging_utility.get_default_logger("service.repository.crunchy"),
        remote_source=RemoteSourceContainer.token_source(),
        time_utility=AppContainer.time_zone_utility(),
    )

    singing_repository = providers.Singleton(
        SingingRepository,
        logger=__logging_utility.get_default_logger("service.repository.crunchy"),
        remote_source=RemoteSourceContainer.signing_source(),
        auth_repository=authentication_repository(),
        time_utility=AppContainer.time_zone_utility()
    )

    cms_repository = providers.Singleton(
        CmsRepository,
        logger=__logging_utility.get_default_logger("service.repository.crunchy"),
        remote_source=RemoteSourceContainer.cms_source(),
    )

    bucket_repository = providers.Singleton(
        BucketRepository,
        logger=__logging_utility.get_default_logger("service.repository.crunchy"),
        remote_source=RemoteSourceContainer.bucket_source(),
    )


class UseCaseContainer(containers.DeclarativeContainer):
    """IoC container for use-cases"""
    __logging_utility = AppContainer.logging_utility()

    use_case = providers.Factory(
        CrunchyUseCase,
        logger=__logging_utility.get_default_logger("service.use_case.crunchy"),
        repository=RepositoryContainer.bucket_repository()
    )

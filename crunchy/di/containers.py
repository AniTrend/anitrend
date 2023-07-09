import dependency_injector.containers as containers
import dependency_injector.providers as providers
from uplink.auth import ApiTokenHeader

from di import CoreContainer
from ..data.repositories import BucketRepository, CmsRepository, SingingRepository, AuthenticationRepository
from ..data.sources import TokenEndpoint, SigningEndpoint, CmsEndpoint, BucketEndpoint
from ..domain.usecases import CrunchyUseCase


class RemoteSourceContainer(containers.DeclarativeContainer):
    """IoC container of remote sources providers"""
    token_source = providers.Singleton(
        TokenEndpoint,
        base_url="https://beta-api.crunchyroll.com/",
        client=CoreContainer.session,
        auth=ApiTokenHeader(header="Authorization", token=CoreContainer.config.CRUNCHY_TOKEN, prefix="Basic")
    )
    cms_source = providers.Singleton(
        CmsEndpoint,
        base_url="https://beta-api.crunchyroll.com/",
        client=CoreContainer.session,
    )
    signing_source = providers.Singleton(
        SigningEndpoint,
        base_url="https://beta-api.crunchyroll.com/",
        client=CoreContainer.session,
    )
    bucket_source = providers.Singleton(
        BucketEndpoint,
        base_url="https://beta-api.crunchyroll.com/",
        client=CoreContainer.session,
    )


class RepositoryContainer(containers.DeclarativeContainer):
    """IoC container of repository providers"""

    authentication_repository = providers.Singleton(
        AuthenticationRepository,
        remote_source=RemoteSourceContainer.token_source(),
        time_utility=CoreContainer.time_zone_utility(),
    )

    signing_repository = providers.Singleton(
        SingingRepository,
        remote_source=RemoteSourceContainer.signing_source(),
        auth_repository=authentication_repository(),
        time_utility=CoreContainer.time_zone_utility()
    )

    cms_repository = providers.Singleton(
        CmsRepository,
        auth_repository=authentication_repository(),
        remote_source=RemoteSourceContainer.cms_source(),
    )

    bucket_repository = providers.Singleton(
        BucketRepository,
        remote_source=RemoteSourceContainer.bucket_source(),
        cms_repository=cms_repository(),
        signing_repository=signing_repository(),
        auth_repository=authentication_repository(),
    )


class UseCaseContainer(containers.DeclarativeContainer):
    """IoC container for use-cases"""

    use_case = providers.Factory(
        CrunchyUseCase,
        repository=RepositoryContainer.bucket_repository()
    )

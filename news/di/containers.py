from dependency_injector import containers, providers
from django.conf import settings

from news.data.repositories import NewsRepository
from news.data.sources import RemoteSource
from news.domain.usecases import NewsUseCase


class NewsContainer(containers.DeclarativeContainer):
    remote_source = providers.Singleton(
        RemoteSource,
        base_url=settings.ON_THE_EDGE['host']
    )

    repository = providers.Singleton(
        NewsRepository,
        remote_source=remote_source
    )

    use_case = providers.Factory(
        NewsUseCase,
        repository=repository
    )
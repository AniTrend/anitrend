import dependency_injector.containers as containers
import dependency_injector.providers as providers
from django.conf import settings

from episode.data.repositories import EpisodeRepository
from episode.data.sources import RemoteSource
from episode.domain.usecases import EpisodeUseCase


class EpisodeContainer(containers.DeclarativeContainer):
    remote_source = providers.Singleton(
        RemoteSource,
        base_url=settings.ON_THE_EDGE["host"],
    )

    repository = providers.Singleton(
        EpisodeRepository,
        remote_source=remote_source,
    )

    use_case = providers.Factory(
        EpisodeUseCase,
        repository=repository,
    )

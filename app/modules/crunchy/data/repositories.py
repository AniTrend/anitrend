from json import JSONDecodeError
from logging import Logger
from typing import Optional, Any, List

from django.db.models import QuerySet
from uplink import Consumer

from app.modules.common import AttributeDictionary
from app.modules.common.errors import NoDataError
from app.modules.common.repositories import DataRepository

from ..domain.entities import CrunchyToken as Token, CrunchySigningPolicyContainer as SigningPolicyContainer, \
    CrunchyPanelCollection as PanelCollection, CrunchySeasonCollection as SeasonCollection, \
    CrunchyEpisodeCollection as EpisodeCollection, CrunchySeries as Series
from ..data.sources import TokenEndpoint, SigningEndpoint, CmsEndpoint, BucketEndpoint
from ..models import CrunchyToken, CrunchySigningPolicy, CrunchySeries, CrunchySeason, CrunchyEpisode, \
    CrunchyPanel, CrunchySeriesPanel, CrunchyMoviePanel


class AuthenticationRepository(DataRepository):
    _remote_source: TokenEndpoint

    def __init__(self, logger: Logger, remote_source: Consumer) -> None:
        super().__init__(logger, remote_source)
        self.__authentication: QuerySet = CrunchyToken.objects


class SingingRepository(DataRepository):
    _remote_source: SigningEndpoint

    def __init__(self, logger: Logger, remote_source: Consumer) -> None:
        super().__init__(logger, remote_source)
        self.__signing_policy: QuerySet = CrunchySigningPolicy.objects


class CmsRepository(DataRepository):
    _remote_source: CmsEndpoint

    def __init__(self, logger: Logger, remote_source: Consumer) -> None:
        super().__init__(logger, remote_source)
        self.__panel: QuerySet = CrunchyPanel.objects
        self.__series_panel: QuerySet = CrunchySeriesPanel.objects
        self.__movie_panel: QuerySet = CrunchyMoviePanel.objects


class BucketRepository(DataRepository):
    _remote_source: BucketEndpoint

    def __init__(self, logger: Logger, remote_source: Consumer) -> None:
        super().__init__(logger, remote_source)
        self.__series: QuerySet = CrunchySeries.objects
        self.__season: QuerySet = CrunchySeason.objects
        self.__episode: QuerySet = CrunchyEpisode.objects

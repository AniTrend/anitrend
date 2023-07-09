from typing import Optional

from django.db.models import QuerySet

from core.errors import NoArgumentError
from core.repositories import RepositoryMixin
from . import MediaParams, SeasonParams
from ..models import Media, Season


class MediaRepository(RepositoryMixin):

    def __init__(self) -> None:
        self.__media = Media.objects
        self.__season = Season.objects

    def get_by_param(self, param: MediaParams) -> Optional[Media]:
        query_set: Optional[QuerySet] = None
        if param.tvdb is not None:
            query_set = self.__media.filter(source__tvdb=param.tvdb)
        elif param.anilist is not None:
            query_set = self.__media.filter(source__anilist=param.anilist)
        elif param.anidb is not None:
            query_set = self.__media.filter(source__anidb=param.anidb)
        elif param.animeplanet is not None:
            query_set = self.__media.filter(source__animeplanet=param.animeplanet)
        elif param.notify is not None:
            query_set = self.__media.filter(source__notify=param.notify)
        elif param.kitsu is not None:
            query_set = self.__media.filter(source__kitsu=param.kitsu)
        elif param.mal is not None:
            query_set = self.__media.filter(source__mal=param.mal)

        if query_set is None:
            self._logger.warning("A minimum of one argument is required")
            raise NoArgumentError("A minimum of one argument is required")
        self._logger.debug(f"Filter query -> {query_set.query}")
        return query_set.first()

    def get_by_season_param(self, param: SeasonParams) -> Optional[Season]:
        query_set: Optional[QuerySet] = None
        if param.mediaId is not None:
            query_set = self.__season.filter(media__id=param.mediaId)

        if query_set is None:
            self._logger.warning("A minimum of one argument is required")
            raise NoArgumentError("A minimum of one argument is required")
        self._logger.debug(f"Filter query -> {query_set.query}")
        return query_set.first()

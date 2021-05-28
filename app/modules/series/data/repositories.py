from logging import Logger
from typing import Optional

from django.db.models import QuerySet

from app.modules.common.repositories import CommonRepository
from app.modules.common.errors import NoArgumentError

from . import SeriesParams, SeasonParams
from ..models import Series, Season


class SeriesRepository(CommonRepository):

    def __init__(self, logger: Logger) -> None:
        super().__init__(logger)
        self.__series = Series.objects
        self.__season = Season.objects

    def get_by_param(self, param: SeriesParams) -> Optional[Series]:
        query_set: Optional[QuerySet] = None
        if param.tvdb is not None:
            query_set = self.__series.filter(source__tvdb=param.tvdb)
        elif param.anilist is not None:
            query_set = self.__series.filter(source__anilist=param.anilist)
        elif param.anidb is not None:
            query_set = self.__series.filter(source__anidb=param.anidb)
        elif param.animeplanet is not None:
            query_set = self.__series.filter(source__animeplanet=param.animeplanet)
        elif param.notify is not None:
            query_set = self.__series.filter(source__notify=param.notify)
        elif param.kitsu is not None:
            query_set = self.__series.filter(source__kitsu=param.kitsu)
        elif param.mal is not None:
            query_set = self.__series.filter(source__mal=param.mal)

        if query_set is None:
            self._logger.warning("A minimum of one argument is required")
            raise NoArgumentError("A minimum of one argument is required")
        self._logger.debug(f"Filter query -> {query_set.query}")
        return query_set.first()

    def get_by_season_param(self, param: SeasonParams) -> Optional[Season]:
        query_set: Optional[QuerySet] = None
        if param.seriesId is not None:
            query_set = self.__season.filter(series__id=param.seriesId)

        if query_set is None:
            self._logger.warning("A minimum of one argument is required")
            raise NoArgumentError("A minimum of one argument is required")
        self._logger.debug(f"Filter query -> {query_set.query}")
        return query_set.first()

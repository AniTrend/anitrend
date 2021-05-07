from dataclasses import dataclass
from logging import Logger
from typing import Optional, List

from dependency_injector.wiring import inject
from django.db.models import QuerySet
from common.contracts import CommonRepository
from api.exceptions import NoArgumentsError
from api.models import Series


@dataclass
class SeriesParams:
    tvdb: Optional[int]
    anidb: Optional[int]
    anilist: Optional[int]
    animeplanet: Optional[str]
    notify: Optional[str]
    kitsu: Optional[int]
    mal: Optional[int]


# noinspection PyProtectedMember
class SeriesRepository(CommonRepository):

    @inject
    def __init__(self, logger: Logger) -> None:
        super().__init__(logger)
        self._local_source = Series.objects

    def save_one(self, series: Series):
        self._local_source.save(series)

    def save_many(self, series_list: List[Series]):
        self._local_source.bulk_create(series_list)

    def get_by_param(self, param: SeriesParams) -> Optional[Series]:
        query_set: Optional[QuerySet] = None
        if param.tvdb is not None:
            query_set = self._local_source.filter(source__tvdb=param.tvdb)
        elif param.anilist is not None:
            query_set = self._local_source.filter(source__anilist=param.anilist)
        elif param.anidb is not None:
            query_set = self._local_source.filter(source__anidb=param.anidb)
        elif param.animeplanet is not None:
            query_set = self._local_source.filter(source__animeplanet=param.animeplanet)
        elif param.notify is not None:
            query_set = self._local_source.filter(source__notify=param.notify)
        elif param.kitsu is not None:
            query_set = self._local_source.filter(source__kitsu=param.kitsu)
        elif param.mal is not None:
            query_set = self._local_source.filter(source__mal=param.mal)

        if query_set is None:
            self._logger.warning("A minimum of one argument is required")
            raise NoArgumentsError("A minimum of one argument is required")
        self._logger.debug(f"Filter query -> {query_set.query}")
        return query_set.first()

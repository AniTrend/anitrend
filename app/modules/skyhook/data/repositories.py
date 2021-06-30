from json import JSONDecodeError
from logging import Logger
from typing import Optional, Any, List, Dict

from django.db.models import QuerySet
from uplink import Consumer

from app.modules.common import AttributeDictionary
from app.modules.common.errors import NoDataError
from app.modules.common.repositories import DataRepository


from ..domain.entities import SkyhookShow, SkyhookImage
from ..data.sources import RemoteSource
from ..models import Show, Image, Episode, Season


class Repository(DataRepository):
    _remote_source: RemoteSource

    def __init__(self, logger: Logger, remote_source: Consumer) -> None:
        super().__init__(logger, remote_source)
        self.__show: QuerySet = Show.objects
        self.__image: QuerySet = Image.objects
        self.__episode: QuerySet = Episode.objects
        self.__season: QuerySet = Season.objects

    @staticmethod
    def __get_image_by_type(images: List[SkyhookImage], image_type: str) -> Optional[str]:
        for image in images:
            if image.coverType == image_type:
                return image.url
        return None

    @staticmethod
    def __get_season_by_number(season_map: Dict, season_number: int) -> Optional[Season]:
        season_number_key = f"{season_number}"
        if season_number_key in season_map:
            return season_map[season_number_key]
        return None

    def map_and_save_results(self, show: SkyhookShow) -> Any:
        self._logger.info(f"Mapping and save results starting")

        _show_image, show_image_created = self.__image.update_or_create(
            banner=self.__get_image_by_type(show.images, "Banner"),
            poster=self.__get_image_by_type(show.images, "Poster"),
            fan_art=self.__get_image_by_type(show.images, "Fanart"),
        )

        _show, _show_created = self.__show.update_or_create(
            tvdb_id=show.tvdbId,
            title=show.title,
            overview=show.overview,
            slug=show.slug,
            first_aired=show.firstAired,
            tv_maze_id=show.tvMazeId,
            added=show.added,
            last_updated=show.lastUpdated,
            status=show.status,
            runtime=show.runtime,
            time_of_day=f"{show.timeOfDay.hours}:{show.timeOfDay.minutes}",
            network=show.network,
            imdb_id=show.imdbId,
            genres=show.genres,
            content_rating=show.contentRating,
            rating=show.rating.value,
            alternative_titles=show.alternativeTitles,
            image=_show_image,
        )

        if _show_created:
            self._logger.info(f"Added new entry -> {_show.title}")
        else:
            self._logger.info(f"Updated entry -> {_show.title}")

        _seasons_map = dict()
        for season in show.seasons:
            _season_image, season_image_created = self.__image.update_or_create(
                banner=self.__get_image_by_type(season.images, "Banner"),
                poster=self.__get_image_by_type(season.images, "Poster"),
                fan_art=self.__get_image_by_type(season.images, "Fanart"),
            )

            _show_season, _show_season_created = self.__season.update_or_create(
                season_number=season.seasonNumber,
                show=_show,
                image=_season_image,
            )
            _seasons_map[f"{season.seasonNumber}"] = _show_season

        for episode in show.episodes:
            _show_episode, _show_episode_created = self.__episode.update_or_create(
                tvdb_show_id=episode.tvdbShowId,
                tvdb_id=episode.tvdbId,
                season=self.__get_season_by_number(_seasons_map, episode.seasonNumber),
                episode_number=episode.episodeNumber,
                aired_after_season=self.__get_season_by_number(_seasons_map, episode.airedAfterSeasonNumber),
                title=episode.title,
                air_date=episode.airDate,
                air_date_utc=episode.airDateUtc,
                overview=episode.overview,
                writers=episode.writers,
                directors=episode.directors,
                image=episode.image,
            )

        return {
            "created": _show_created,
            "updated": _show
        }

    def __on_result(self, data: SkyhookShow):
        if data is not None:
            return self.map_and_save_results(data)
        else:
            raise NoDataError(f"Data received for anime entries was null")

    def invoke(self, **kwargs) -> Optional[Any]:
        try:
            data = self._remote_source.get_show_by_tvdb(kwargs.pop("tvdb_id"))
            return self.__on_result(data)
        except JSONDecodeError as e:
            self._logger.error(f"Malformed response with error message `{e.doc}`", exc_info=e)
            raise e

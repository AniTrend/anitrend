from json import JSONDecodeError
from logging import Logger
from typing import Optional, Any, List

from django.db.models import QuerySet
from uplink import Consumer

from app.modules.common import AttributeDictionary
from app.modules.common.errors import NoDataError
from app.modules.common.utilities import LinkUtility
from app.modules.common.repositories import DataRepository

from ..domain.entities import AnimeContainer, AnimeData
from ..data.sources import RemoteSource
from ..models import Anime, AnimeSource, AnimeRelation


class Repository(DataRepository):
    _remote_source: RemoteSource

    def __init__(self, logger: Logger, remote_source: Consumer) -> None:
        super().__init__(logger, remote_source)
        self.__anime: QuerySet = Anime.objects
        self.__anime_source: QuerySet = AnimeSource.objects
        self.__anime_relations: QuerySet = AnimeRelation.objects

    @staticmethod
    def __create_attributes_from_links(links: List[str]) -> AttributeDictionary:
        attr_dictionary = AttributeDictionary()
        attr_dictionary.anidb = LinkUtility.extract_id_if_matches(links, "anidb.net")
        attr_dictionary.anilist = LinkUtility.extract_id_if_matches(links, "anilist.co")
        attr_dictionary.animeplanet = LinkUtility.extract_id_if_matches(links, "anime-planet.com")
        attr_dictionary.kitsu = LinkUtility.extract_id_if_matches(links, "kitsu.io")
        attr_dictionary.mal = LinkUtility.extract_id_if_matches(links, "myanimelist.net")
        attr_dictionary.notify = LinkUtility.extract_id_if_matches(links, "notify.moe")
        return attr_dictionary

    def map_and_save_results(self, container: AnimeContainer) -> Any:
        created_records: int = 0
        updated_records: int = 0
        self._logger.info(f"Mapping and save results starting")
        for data in container.data:
            data: AnimeData
            _sources_attribute = self.__create_attributes_from_links(data.sources)
            _anime_source, _anime_source_created = self.__anime_source.update_or_create(
                anidb=_sources_attribute.anidb,
                anilist=_sources_attribute.anilist,
                animeplanet=_sources_attribute.animeplanet,
                kitsu=_sources_attribute.kitsu,
                mal=_sources_attribute.mal,
                notify=_sources_attribute.notify,
            )

            _anime, _anime_created = self.__anime.update_or_create(
                title=data.title,
                source=_anime_source,
                year=data.animeSeason.year,
                season=data.animeSeason.season,
                type=data.type,
                episodes=data.episodes,
                status=data.status,
                picture=data.picture,
                thumbnail=data.thumbnail,
            )

            if _anime_created:
                created_records += 1
                self._logger.info(f"Added new entry -> {_anime.title}")
            else:
                updated_records += 1
                self._logger.info(f"Updated entry -> {_anime.title}")

            for relation_url in data.relations:
                self.__anime_relations.update_or_create(
                    url=relation_url,
                    anime=_anime
                )

        return {
            "created": created_records,
            "updated": updated_records
        }

    def __on_result(self, data: AnimeContainer):
        if data is not None:
            return self.map_and_save_results(data)
        else:
            raise NoDataError(f"Data received for anime entries was null")

    def invoke(self) -> Optional[Any]:
        try:
            data = self._remote_source.get_anime_entries()
            return self.__on_result(data)
        except JSONDecodeError as e:
            self._logger.error(f"Malformed response with error message `{e.doc}`", exc_info=e)
            raise e

from json import JSONDecodeError
from logging import Logger
from typing import Optional, Any, List

from uplink import Consumer
from api.models import Series, Source, Relation, Synonym, Tag
from common import AttributeDictionary
from common.utilities import RegexUtility
from service.models import Mapping, MappingTitle
from common.contracts import CommonRepository
from data.remote_sources import XemRemoteSource, RelationRemoteSource
from data.model_entities import RelationContainerEntity, XemContainerEntity, RelationDataEntity


class IRepository(CommonRepository):

    def __init__(self, logger: Logger, remote_source: Consumer) -> None:
        super().__init__(logger)
        self._remote_source = remote_source

    def map_and_save_results(self, entity: Any):
        """
        Processes an entity and saves the results
        :param entity: Entity containing data which needs to be mapped
        """
        pass

    def invoke(self) -> Optional[List]:
        """
        Requests data from a remote source
        :return: Optional items
        """
        pass


class XemRepository(IRepository):
    _remote_source: XemRemoteSource

    def __init__(self, logger: Logger, remote_source: Consumer) -> None:
        super().__init__(logger, remote_source)
        self._local_source = MappingTitle.objects

    def map_and_save_results(self, entity: XemContainerEntity):
        for _id, _titles in entity.data.items():
            mapping, created = Mapping.objects.update_or_create(id=_id)
            self._logger.debug(f"Saved `{mapping}` and creation status: {created}")
            for title in _titles:
                mapping_title, created = self._local_source.update_or_create(
                    title=title,
                    mapping=mapping
                )
                self._logger.debug(f"Saved `{mapping_title}` and creation status: {created}")

    def invoke(self) -> Optional[XemContainerEntity]:
        try:
            result = self._remote_source.get_all_names(
                origin="tvdb",
                language="all",
                default_names=1
            )
            return result
        except JSONDecodeError as e:
            self._logger.error(f"Malformed response with error message `{e.doc}`", exc_info=e)

        return None


class RelationRepository(IRepository):
    _remote_source: RelationRemoteSource

    def __init__(self, logger: Logger, remote_source: Consumer) -> None:
        super().__init__(logger, remote_source)
        self._local_source = Series.objects

    @staticmethod
    def __create_attributes_from_links(links: List[str]) -> AttributeDictionary:
        attr_dictionary = AttributeDictionary()
        attr_dictionary.tvdb = RegexUtility.extract_id_if_matches(links, "thetvdb.com")
        attr_dictionary.anidb = RegexUtility.extract_id_if_matches(links, "anidb.net")
        attr_dictionary.anilist = RegexUtility.extract_id_if_matches(links, "anilist.co")
        attr_dictionary.animeplanet = RegexUtility.extract_id_if_matches(links, "anime-planet.com")
        attr_dictionary.kitsu = RegexUtility.extract_id_if_matches(links, "kitsu.io")
        attr_dictionary.mal = RegexUtility.extract_id_if_matches(links, "myanimelist.net")
        attr_dictionary.notify = RegexUtility.extract_id_if_matches(links, "notify.moe")
        return attr_dictionary

    def map_and_save_results(self, entity: RelationContainerEntity):
        for item in entity.data:
            item: RelationDataEntity
            _sources = self.__create_attributes_from_links(item.sources)

            source, created = Source.objects.update_or_create(
                tvdb=_sources.tvdb,
                anidb=_sources.anidb,
                anilist=_sources.anilist,
                animeplanet=_sources.animeplanet,
                kitsu=_sources.kitsu,
                mal=_sources.mal,
                notify=_sources.notify,
            )
            self._logger.debug(f"Saved `{source}` and creation status: {created}")

            series, created = self._local_source.update_or_create(
                title=item.title,
                source=source,
                type=item.type,
                episodes=item.episodes,
                status=item.status,
                picture=item.picture,
                thumbnail=item.thumbnail,
            )
            self._logger.debug(f"Saved `{series}` and creation status: {created}")

            for relation in item.relations:
                obj, created = Relation.objects.update_or_create(
                    url=relation,
                    series=series
                )
                self._logger.debug(f"Saved `{obj}` and creation status: {created}")

            for synonym in item.synonyms:
                obj, created = Synonym.objects.update_or_create(
                    title=synonym,
                    series=series
                )
                self._logger.debug(f"Saved `{obj}` and creation status: {created}")

            for tag in item.tags:
                obj, created = Tag.objects.update_or_create(
                    title=tag,
                    series=series
                )
                self._logger.debug(f"Saved `{obj}` and creation status: {created}")

    def invoke(self) -> Optional[RelationContainerEntity]:
        try:
            result = self._remote_source.get_anime_entries()
            return result
        except JSONDecodeError as e:
            self._logger.error(f"Malformed response with error message `{e.doc}`", exc_info=e)

        return None

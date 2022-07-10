from json import JSONDecodeError
from logging import Logger
from typing import Optional, Any, List, Tuple, Dict

from django.db.models import QuerySet
from pyxtension.streams import stream
from uplink import Consumer

from app.modules.common import AttributeDictionary, TimeUtility
from app.modules.common.errors import NoDataError
from app.modules.common.repositories import DataRepository
from .schemas import IndexContainerSchema, SigningPolicySchema

from ..domain.entities import CrunchyToken as Token, CrunchySigningPolicyContainer as SigningPolicyContainer, \
    CrunchyPanelCollection as PanelCollection, CrunchySeasonCollection as SeasonCollection, \
    CrunchyEpisodeCollection as EpisodeCollection, CrunchySeries as Series, CrunchyMovieMeta as MovieMeta, \
    CrunchySeriesMeta as SeriesMeta, CrunchyBrowseContainer as BrowseContainer, \
    CrunchyIndexContainer as IndexContainer, CrunchyIndex as Index, CrunchyPanel as Panel, \
    CrunchyImageContainer as ImageContainer
from ..data.sources import TokenEndpoint, SigningEndpoint, CmsEndpoint, BucketEndpoint
from ..models import CrunchyToken, CrunchySigningPolicy, CrunchySeries, CrunchySeason, CrunchyEpisode, \
    CrunchyPanel, CrunchySeriesMeta, CrunchyMovieMeta, CrunchyIndex


class AuthenticationRepository(DataRepository):
    _remote_source: TokenEndpoint

    def __init__(self, logger: Logger, remote_source: Consumer, time_utility: TimeUtility) -> None:
        super().__init__(logger, remote_source)
        self.__authentication: QuerySet = CrunchyToken.objects
        self.__time_utility = time_utility

    def __assure_only_valid_token_exist(self) -> None:
        _deleted, deleted_count = self.__authentication.filter(
            expires_at__lt=self.__time_utility.get_current_timestamp()
        ).delete()
        if deleted_count > 0:
            self._logger.debug(
                f"Invalidated database items with and returned result: {deleted_count}"
            )

    def __get_latest_token(self) -> Optional[CrunchyToken]:
        _token_filter = self.__authentication.filter(
            expires_at__gt=self.__time_utility.get_current_timestamp()
        )
        _token = _token_filter.first()
        self._logger.debug(f"Current valid token: {_token}")
        return _token

    def __map_and_save(self, token):
        current_time_stamp = self.__time_utility.get_current_timestamp()
        future_expiry_time = current_time_stamp + token.expires_in
        _token, _created = self.__authentication.update_or_create(
            access_token=token.access_token,
            expires_at=future_expiry_time,
            token_type=token.token_type,
            country=token.country,
        )
        if _created:
            self._logger.debug(f"Saved token successfully: {_token}")

    def __make_request(self) -> Optional[Any]:
        token = self._remote_source.get_authorization_token()
        return token

    def invoke(self, **kwargs) -> Optional[CrunchyToken]:
        self.__assure_only_valid_token_exist()
        last_valid_token = self.__get_latest_token()
        if last_valid_token is None:
            token = self.__make_request()
            self.__map_and_save(token)
            last_valid_token = self.__get_latest_token()
        return last_valid_token

    def get_authorization_header(self) -> Optional[str]:
        token = self.invoke()
        if token is not None:
            return str(token)
        return None


class SingingRepository(DataRepository):
    _remote_source: SigningEndpoint

    def __init__(
            self,
            logger: Logger,
            remote_source: Consumer,
            auth_repository: AuthenticationRepository,
            time_utility: TimeUtility
    ) -> None:
        super().__init__(logger, remote_source)
        self.__signing_policy: QuerySet = CrunchySigningPolicy.objects
        self.__auth_repository = auth_repository
        self.__time_utility = time_utility

    def __make_request(self) -> Optional[SigningPolicySchema]:
        signing_policy = self._remote_source.get_signing_policy(
            authorization=self.__auth_repository.get_authorization_header()
        )
        return signing_policy

    def __map_and_save(self, signing_policy) -> Optional[CrunchySigningPolicy]:
        _model, _created = self.__signing_policy.update_or_create(
            bucket=signing_policy.bucket,
            policy=signing_policy.policy,
            signature=signing_policy.signature,
            key_pair_id=signing_policy.key_pair_id,
            expires=signing_policy.expires,
        )
        if _created:
            self._logger.debug(f"Created signing policy {_model}")
        return _model

    def __assure_only_valid_token_exist(self) -> None:
        _deleted, deleted_count = self.__signing_policy.filter(
            expires=self.__time_utility.get_current_timestamp()
        ).delete()
        if deleted_count > 0:
            self._logger.debug(
                f"Invalidated database items with and returned result: {deleted_count}"
            )

    def __latest_signing_policy(self) -> Optional[CrunchySigningPolicy]:
        return self.__signing_policy.latest()

    def invoke(self, **kwargs) -> Optional[CrunchySigningPolicy]:
        self.__assure_only_valid_token_exist()
        existing = self.__latest_signing_policy()
        if existing is not None:
            return existing
        signing_policy = self.__make_request()
        return self.__map_and_save(signing_policy)


class CmsRepository(DataRepository):
    _remote_source: CmsEndpoint

    def __init__(
            self,
            logger: Logger,
            remote_source: Consumer,
            auth_repository: AuthenticationRepository
    ) -> None:
        super().__init__(logger, remote_source)
        self.__index: QuerySet = CrunchyIndex.objects
        self.__panel: QuerySet = CrunchyPanel.objects
        self.__series_panel: QuerySet = CrunchySeriesMeta.objects
        self.__movie_panel: QuerySet = CrunchyMovieMeta.objects
        self.__auth_repository = auth_repository

    def __make_request(self) -> Optional[IndexContainer]:
        return self._remote_source.get_index(
            authorization=self.__auth_repository.get_authorization_header()
        )

    def __make_panel_request(self, prefix: str, size: int) -> Optional[BrowseContainer]:
        return self._remote_source.get_browse(
            authorization=self.__auth_repository.get_authorization_header(),
            q=prefix,
            n=size
        )

    @staticmethod
    def __map_movie_listing_meta(metadata: Optional[MovieMeta]) -> Optional[CrunchyMovieMeta]:
        if metadata is not None:
            return CrunchyMovieMeta(
                audio_locales=metadata.audio_locales,
                subtitle_locales=metadata.subtitle_locales,
                extended_description=metadata.extended_description,
                slug=metadata.slug,
                title=metadata.title,
                slug_title=metadata.slug_title,
                duration_ms=metadata.duration_ms,
                movie_release_year=metadata.movie_release_year,
                is_premium_only=metadata.is_premium_only,
                is_mature=metadata.is_mature,
                mature_blocked=metadata.mature_blocked,
                is_subbed=metadata.is_subbed,
                is_dubbed=metadata.is_dubbed,
                available_offline=metadata.available_offline,
                maturity_ratings=metadata.maturity_ratings,
                tenant_categories=metadata.tenant_categories,
            )
        return None

    @staticmethod
    def __map_series_listing_meta(metadata: Optional[SeriesMeta]) -> Optional[CrunchySeriesMeta]:
        if metadata is not None:
            return CrunchySeriesMeta(
                audio_locales=metadata.audio_locales,
                subtitle_locales=metadata.subtitle_locales,
                extended_description=metadata.extended_description,
                slug=metadata.slug,
                title=metadata.title,
                slug_title=metadata.slug_title,
                episode_count=metadata.episode_count,
                season_count=metadata.season_count,
                is_mature=metadata.is_mature,
                mature_blocked=metadata.mature_blocked,
                is_subbed=metadata.is_subbed,
                is_dubbed=metadata.is_dubbed,
                is_simulcast=metadata.is_simulcast,
                maturity_ratings=metadata.maturity_ratings,
                tenant_categories=metadata.tenant_categories,
                last_public_season_number=metadata.last_public_season_number,
                last_public_episode_number=metadata.last_public_episode_number,
            )
        return None

    def __map_panels(self, panels: List[Panel]) -> Tuple[int, int]:
        created_records: int = 0
        updated_records: int = 0

        for panel in panels:
            panel: Panel
            _panel, _panel_created = self.__panel.update_or_create(
                panel_id=panel.id,
                external_id=panel.external_id.lstrip("SRZ."),
                channel_id=panel.channel_id,
                title=panel.title,
                description=panel.description,
                type=panel.type,
                slug=panel.slug,
                images=panel.images,
                movie_listing_metadata=self.__map_movie_listing_meta(panel.movie_listing_metadata),
                series_metadata=self.__map_series_listing_meta(panel.series_metadata),
                last_public=panel.last_public,
                new=panel.new,
                new_content=panel.new_content,
            )

            if created_records:
                created_records += 1
                self._logger.info(f"Added new entry -> {_panel.title}")
            else:
                updated_records += 1
                self._logger.info(f"Updated entry -> {_panel.title}")

        return created_records, updated_records

    def map_and_save_results(self, container: IndexContainer) -> Dict:
        created_records: int = 0
        updated_records: int = 0

        self._logger.info(f"Mapping and save results starting")

        for index in container.items:
            index: Index
            _index, _created = self.__index.update_or_create(
                prefix=index.prefix,
                offset=index.offset,
                count=index.count
            )

            if _created:
                created_records += 1
                self._logger.info(f"Added new entry -> {_index}")
            else:
                updated_records += 1
                self._logger.info(f"Updated entry -> {_index}")

        created_panels: int = 0
        updated_panels: int = 0

        if created_records > 0 or updated_records > 0:
            for index in container.items:
                index: Index
                browse_container = self.__make_panel_request(index.prefix, index.num_items)
                created_panels, updated_panels = self.__map_panels(browse_container.items)

        return {
            "index": {
                "created": created_records,
                "updated": updated_records
            },
            "panel": {
                "created": created_panels,
                "updated": updated_panels
            }
        }

    def __on_result(self, data: IndexContainer) -> Dict:
        if data is not None:
            return self.map_and_save_results(data)
        else:
            raise NoDataError(f"Data received for anime entries was null")

    def invoke(self, **kwargs) -> Optional[Any]:
        try:
            data = self.__make_request()
            return self.__on_result(data)
        except JSONDecodeError as e:
            self._logger.error(f"Malformed response with error message `{e.doc}`", exc_info=e)
            raise e


class BucketRepository(DataRepository):
    _remote_source: BucketEndpoint

    def __init__(
            self,
            logger: Logger,
            remote_source: Consumer,
            cms_repository: CmsRepository,
            signing_repository: SingingRepository,
            auth_repository: AuthenticationRepository
    ) -> None:
        super().__init__(logger, remote_source)
        self.__panel: QuerySet = CrunchyPanel.objects
        self.__movie_panel: QuerySet = CrunchyMovieMeta.objects
        self.__series_panel: QuerySet = CrunchySeriesMeta.objects
        self.__cms_repository = cms_repository
        self.__signing_repository = signing_repository
        self.__auth_repository = auth_repository

    def __make_request(self, panel_id: str) -> Optional[CrunchySeries]:
        return self._remote_source.get_series_details(
            authorization=self.__auth_repository.get_authorization_header(),
            series_id=panel_id
        )

    def map_and_save_results(self, container: IndexContainer) -> Any:
        created_records: int = 0
        updated_records: int = 0
        self._logger.info(f"Mapping and save results starting")

        for index in container.items:
            index: Index
            for panel in index.items:
                panel: Panel

                movie_listing = None
                if panel.movie_listing_metadata is not None:
                    generated_id: str = panel.external_id
                    movie_listing, created = self.__movie_panel.update_or_create(
                        id=generated_id,
                        duration_ms=panel.movie_listing_metadata.duration_ms,
                        movie_release_year=panel.movie_listing_metadata.movie_release_year,
                        is_premium_only=panel.movie_listing_metadata.is_premium_only,
                        is_mature=panel.movie_listing_metadata.is_mature,
                        mature_blocked=panel.movie_listing_metadata.mature_blocked,
                        is_subbed=panel.movie_listing_metadata.is_subbed,
                        is_dubbed=panel.movie_listing_metadata.is_dubbed,
                        available_offline=panel.movie_listing_metadata.available_offline,
                        maturity_ratings=panel.movie_listing_metadata.maturity_ratings,
                        tenant_categories=panel.movie_listing_metadata.tenant_categories,
                    )

                series_listing = None
                if panel.series_metadata is not None:
                    generated_id: str = panel.external_id
                    series_listing, created = self.__series_panel.update_or_create(
                        id=generated_id,
                        episode_count=panel.series_metadata.episode_count,
                        season_count=panel.series_metadata.season_count,
                        is_mature=panel.series_metadata.is_mature,
                        mature_blocked=panel.series_metadata.mature_blocked,
                        is_subbed=panel.series_metadata.is_subbed,
                        is_dubbed=panel.series_metadata.is_dubbed,
                        is_simulcast=panel.series_metadata.is_simulcast,
                        maturity_ratings=panel.series_metadata.maturity_ratings,
                        tenant_categories=panel.series_metadata.tenant_categories,
                        last_public_season_number=panel.series_metadata.last_public_season_number,
                    )

                series_images = ImageContainer.to_json(panel.images)

                _panel, panel_created = self.__panel.update_or_create(
                    panel_id=panel.id,
                    external_id=panel.external_id,
                    channel_id=panel.channel_id,
                    title=panel.title,
                    description=panel.description,
                    type=panel.type,
                    slug=panel.slug,
                    images=series_images,
                    movie_listing_metadata=movie_listing,
                    series_metadata=series_listing,
                    last_public=panel.last_public,
                    new=panel.new,
                    new_content=panel.new_content,
                )

                if panel_created:
                    created_records += 1
                    self._logger.info(f"Added new entry -> {_panel.title}")
                else:
                    updated_records += 1
                    self._logger.info(f"Updated entry -> {_panel.title}")

        return {
            "created": created_records,
            "updated": updated_records
        }

    def invoke(self, **kwargs) -> Optional[Any]:
        for panel in self.__panel:
            panel: CrunchyPanel
            self.__make_request(panel.panel_id)

        return self.__make_request()

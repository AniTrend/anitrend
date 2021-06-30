from json import JSONDecodeError
from logging import Logger
from typing import Optional, Any, List

from django.db.models import QuerySet
from uplink import Consumer

from app.modules.common import AttributeDictionary, TimeUtility
from app.modules.common.errors import NoDataError
from app.modules.common.repositories import DataRepository

from ..domain.entities import CrunchyToken as Token, CrunchySigningPolicyContainer as SigningPolicyContainer, \
    CrunchyPanelCollection as PanelCollection, CrunchySeasonCollection as SeasonCollection, \
    CrunchyEpisodeCollection as EpisodeCollection, CrunchySeries as Series, \
    CrunchyIndexContainer as IndexContainer, CrunchyIndex as Index, CrunchyPanel as Panel, \
    CrunchyImageContainer as ImageContainer
from ..data.sources import TokenEndpoint, SigningEndpoint, CmsEndpoint, BucketEndpoint
from ..models import CrunchyToken, CrunchySigningPolicy, CrunchySeries, CrunchySeason, CrunchyEpisode, \
    CrunchyPanel, CrunchySeriesPanel, CrunchyMoviePanel


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
            return f"Bearer {token.access_token}"
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

    def __make_request(self) -> Optional[Any]:
        signing_policy = self._remote_source.get_signing_policy(
            authorization=self.__auth_repository.get_authorization_header()
        )
        return signing_policy

    def __map_and_save(self, signing_policy):
        _model, _created = self.__signing_policy.update_or_create(
            bucket=signing_policy.bucket,
            policy=signing_policy.policy,
            signature=signing_policy.signature,
            key_pair_id=signing_policy.key_pair_id,
            expires=signing_policy.expires,
        )
        if _created:
            self._logger.debug(f"Created signing policy {_model}")

    def __assure_only_valid_token_exist(self) -> None:
        _deleted, deleted_count = self.__signing_policy.filter(
            expires=self.__time_utility.get_current_timestamp()
        ).delete()
        if deleted_count > 0:
            self._logger.debug(
                f"Invalidated database items with and returned result: {deleted_count}"
            )

    def __latest_signing_policy(self) -> Optional[CrunchySigningPolicy]:
        pass

    def invoke(self, **kwargs) -> Optional[CrunchySigningPolicy]:
        return super().invoke(**kwargs)


class CmsRepository(DataRepository):
    _remote_source: CmsEndpoint

    def __init__(self, logger: Logger, remote_source: Consumer) -> None:
        super().__init__(logger, remote_source)
        self.__panel: QuerySet = CrunchyPanel.objects
        self.__series_panel: QuerySet = CrunchySeriesPanel.objects
        self.__movie_panel: QuerySet = CrunchyMoviePanel.objects

    def invoke(self, **kwargs) -> Optional[Any]:
        return super().invoke(**kwargs)


class BucketRepository(DataRepository):
    _remote_source: BucketEndpoint

    def __init__(self, logger: Logger, remote_source: Consumer) -> None:
        super().__init__(logger, remote_source)
        self.__panel: QuerySet = CrunchyPanel.objects
        self.__movie_panel: QuerySet = CrunchyMoviePanel.objects
        self.__series_panel: QuerySet = CrunchySeriesPanel.objects

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
                        id=generated_id.lstrip("SRZ."),
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
                        id=generated_id.lstrip("SRZ."),
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
        return super().invoke(**kwargs)

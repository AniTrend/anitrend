from marshmallow import EXCLUDE
from uplink import get, post, timeout, retry, ratelimit, Consumer, Query, Field, Header, Path

from core.decorators import raise_api_error, retry_and_ratelimit_strategy
from ..data.schemas import TokenSchema, SigningPolicySchema, IndexContainerSchema, \
    BrowseContainerSchema, SeriesSchema, SeasonContainerSchema, EpisodeContainerSchema


@retry_and_ratelimit_strategy
class TokenEndpoint(Consumer):

    @raise_api_error
    @post("auth/v1/token")
    def get_authorization_token(
            self,
            grand_type: Field(name="grant_type", type=str) = "client_id"
    ) -> TokenSchema:
        pass


@retry_and_ratelimit_strategy
class SigningEndpoint(Consumer):

    @raise_api_error
    @get("index/v2")
    def get_signing_policy(
            self,
            authorization: Header(name="Authorization"),
            locale: Query(name="locale", type=str) = "en-US"
    ) -> SigningPolicySchema:
        pass


@retry_and_ratelimit_strategy
class CmsEndpoint(Consumer):

    @raise_api_error
    @get("content/v1/browse/index")
    def get_index(
            self,
            authorization: Header("Authorization"),
            locale: Query(name="locale", type=str) = "en-US"
    ) -> IndexContainerSchema:
        pass

    @raise_api_error
    @get("content/v1/browse")
    def get_browse(
            self,
            authorization: Header("Authorization"),
            q: Query(name="q", type=str),
            sort_by: Query(name="sort_by", type=str) = "alphabetical",
            n: Query(name="n", type=int) = 100,
            locale: Query(name="locale", type=str) = "en-US"
    ) -> BrowseContainerSchema:
        pass


@retry_and_ratelimit_strategy
class BucketEndpoint(Consumer):

    @raise_api_error
    @get("cms/v2/{bucket}/series/{series_id}")
    def get_series_details(
            self,
            authorization: Header("Authorization"),
            bucket: Path(name="bucket", type=str),
            series_id: Path(name="series_id", type=str),
            locale: Query(name="locale", type=str) = "en-US"
    ) -> SeriesSchema:
        pass

    @raise_api_error
    @get("cms/v2/{bucket}/seasons")
    def get_seasons(
            self,
            authorization: Header("Authorization"),
            bucket: Path(name="bucket", type=str),
            series_id: Query(name="series_id", type=str),
            locale: Query(name="locale", type=str) = "en-US"
    ) -> SeasonContainerSchema:
        pass

    @raise_api_error
    @get("cms/v2/{bucket}/episodes")
    def get_episodes(
            self,
            authorization: Header("Authorization"),
            bucket: Path(name="bucket", type=str),
            season_id: Query(name="season_id", type=str),
            locale: Query(name="locale", type=str) = "en-US"
    ) -> EpisodeContainerSchema:
        pass

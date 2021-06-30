from uplink import get, post, timeout, retry, ratelimit, Consumer, Query, Field, Header, Path
from marshmallow import EXCLUDE

from app.modules.common.decorators import raise_api_error
from ..data.schemas import TokenSchema, SigningPolicySchema, IndexContainerSchema, \
    PanelSchema, SeriesSchema, SeasonContainerSchema, EpisodeContainerSchema

__TIME_OUT__: int = 180
__MAX_ATTEMPTS__: int = 5
__RATE_LIMIT_CALLS__: int = 5
__RATE_LIMIT_PERIOD_CALLS__: int = 10


@timeout(seconds=__TIME_OUT__)
@retry(
    max_attempts=__MAX_ATTEMPTS__,
    when=retry.when.raises(Exception),
    stop=retry.stop.after_attempt(__MAX_ATTEMPTS__) | retry.stop.after_delay(__RATE_LIMIT_PERIOD_CALLS__),
    backoff=retry.backoff.jittered(multiplier=0.5)
)
@ratelimit(
    calls=__RATE_LIMIT_CALLS__,
    period=__RATE_LIMIT_PERIOD_CALLS__
)
class TokenEndpoint(Consumer):

    @raise_api_error
    @post("auth/v1/token")
    def get_authorization_token(
            self,
            grand_type: Field(name="grant_type", type=str) = "client_id"
    ) -> TokenSchema(unknown=EXCLUDE):
        pass


@timeout(seconds=__TIME_OUT__)
@retry(
    max_attempts=__MAX_ATTEMPTS__,
    when=retry.when.raises(Exception),
    stop=retry.stop.after_attempt(__MAX_ATTEMPTS__) | retry.stop.after_delay(__RATE_LIMIT_PERIOD_CALLS__),
    backoff=retry.backoff.jittered(multiplier=0.5)
)
@ratelimit(
    calls=__RATE_LIMIT_CALLS__,
    period=__RATE_LIMIT_PERIOD_CALLS__
)
class SigningEndpoint(Consumer):

    @raise_api_error
    @get("index/v2")
    def get_signing_policy(
            self,
            authorization: Header(name="Authorization"),
            locale: Query(name="locale", type=str) = "en-US"
    ) -> SigningPolicySchema(unknown=EXCLUDE):
        pass


@timeout(seconds=__TIME_OUT__)
@retry(
    max_attempts=__MAX_ATTEMPTS__,
    when=retry.when.raises(Exception),
    stop=retry.stop.after_attempt(__MAX_ATTEMPTS__) | retry.stop.after_delay(__RATE_LIMIT_PERIOD_CALLS__),
    backoff=retry.backoff.jittered(multiplier=0.5)
)
@ratelimit(
    calls=__RATE_LIMIT_CALLS__,
    period=__RATE_LIMIT_PERIOD_CALLS__
)
class CmsEndpoint(Consumer):

    @raise_api_error
    @get("content/v1/browse/index")
    def get_panel(
            self,
            authorization: Header("Authorization"),
            locale: Query(name="locale", type=str) = "en-US"
    ) -> PanelSchema(unknown=EXCLUDE):
        pass

    @raise_api_error
    @get("content/v1/browse")
    def get_index(
            self,
            authorization: Header("Authorization"),
            q: Query(name="q", type=str),
            sort_by: Query(name="sort_by", type=str) = "alphabetical",
            n: Query(name="n", type=int) = 100,
            locale: Query(name="locale", type=str) = "en-US"
    ) -> IndexContainerSchema(unknown=EXCLUDE):
        pass


@timeout(seconds=__TIME_OUT__)
@retry(
    max_attempts=__MAX_ATTEMPTS__,
    when=retry.when.raises(Exception),
    stop=retry.stop.after_attempt(__MAX_ATTEMPTS__) | retry.stop.after_delay(__RATE_LIMIT_PERIOD_CALLS__),
    backoff=retry.backoff.jittered(multiplier=0.5)
)
@ratelimit(
    calls=__RATE_LIMIT_CALLS__,
    period=__RATE_LIMIT_PERIOD_CALLS__
)
class BucketEndpoint(Consumer):

    @raise_api_error
    @get("cms/v2/{bucket}/series/{series_id}")
    def get_series_details(
            self,
            authorization: Header("Authorization"),
            bucket: Path(name="bucket", type=str),
            series_id: Path(name="series_id", type=str),
            locale: Query(name="locale", type=str) = "en-US"
    ) -> SeriesSchema(unknown=EXCLUDE):
        pass

    @raise_api_error
    @get("cms/v2/{bucket}/seasons")
    def get_seasons(
            self,
            authorization: Header("Authorization"),
            bucket: Path(name="bucket", type=str),
            series_id: Query(name="series_id", type=str),
            locale: Query(name="locale", type=str) = "en-US"
    ) -> SeasonContainerSchema(unknown=EXCLUDE):
        pass

    @raise_api_error
    @get("cms/v2/{bucket}/episodes")
    def get_episodes(
            self,
            authorization: Header("Authorization"),
            bucket: Path(name="bucket", type=str),
            season_id: Query(name="season_id", type=str),
            locale: Query(name="locale", type=str) = "en-US"
    ) -> EpisodeContainerSchema(unknown=EXCLUDE):
        pass

    @raise_api_error
    @get("cms/v2/{bucket}/episodes")
    def get_episodes(
            self,
            authorization: Header("Authorization"),
            bucket: Path(name="bucket", type=str),
            season_id: Query(name="season_id", type=str),
            locale: Query(name="locale", type=str) = "en-US"
    ) -> EpisodeContainerSchema(unknown=EXCLUDE):
        pass

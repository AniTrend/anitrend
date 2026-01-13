from typing import Mapping, Type
from marshmallow import EXCLUDE
from marshmallow_dataclass import class_schema
from uplink import (
    Query,
    get,
    returns,
    timeout,
    retry,
    ratelimit,
    Consumer,
    HeaderMap,
    install,
    loads,
)

from core.decorators import raise_api_error
from core import (
    __TIME_OUT__,
    __MAX_ATTEMPTS__,
    __RATE_LIMIT_CALLS__,
    __RATE_LIMIT_PERIOD_CALLS__,
)
from media.data.schemas import MediaEntity


@install
@loads.from_json(MediaEntity)
def load_model_from_json(
    model_type: Type[MediaEntity], json: Mapping[str, any]
) -> MediaEntity:
    # Using marshmallow_dataclass to load directly into dataclass
    # This assumes the JSON keys match the dataclass field names
    schema = class_schema(model_type)()
    result = schema.load(json, unknown=EXCLUDE)  # EXCLUDE unknown fields
    return result  # type: ignore


@timeout(seconds=__TIME_OUT__)
@retry(
    max_attempts=__MAX_ATTEMPTS__,
    when=retry.when.raises(Exception),
    stop=retry.stop.after_attempt(__MAX_ATTEMPTS__)
    | retry.stop.after_delay(10),  # Increased delay slightly
    backoff=retry.backoff.jittered(multiplier=2),
)
@ratelimit(calls=__RATE_LIMIT_CALLS__, period=__RATE_LIMIT_PERIOD_CALLS__)
class RemoteSource(Consumer):

    @returns.from_json  # Expecting JSON response, will be processed by load_model_from_json
    @raise_api_error
    @get("v1/series")
    def get_series(
        self,
        headers: HeaderMap,
        anilist: Query(name="anilist", type=int) = None,
        trakt: Query(name="trakt", type=int) = None,
        tvdb: Query(name="tvdb", type=int) = None,
        tmdb: Query(name="tmdb", type=int) = None,
        mal: Query(name="mal", type=int) = None,
        notify: Query(name="notify", type=str) = None,
        slug: Query(name="slug", type=str) = None,
    ) -> MediaEntity:  # type: ignore
        """
        Fetch aggregated series metadata using upstream identifiers.
        :param headers: Request headers
        :param anilist: AniList series identifier (required by upstream service)
        :param trakt: Trakt identifier
        :param tvdb: TVDB identifier
        :param tmdb: TMDB identifier
        :param mal: MyAnimeList identifier
        :param notify: notify.moe identifier
        :param slug: Slug identifier
        :return: MediaEntity
        """
        pass

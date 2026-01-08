from typing import Mapping, Type
from marshmallow import EXCLUDE, Schema
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
from episode.data.schemas import EpisodesResponse


@install
@loads.from_json(EpisodesResponse)
def load_model_from_json(
    model_type: Type[EpisodesResponse], json: Mapping[str, object]
) -> EpisodesResponse:
    schema: Schema = class_schema(model_type)()
    result: EpisodesResponse = schema.load(json, unknown=EXCLUDE)
    return result


@timeout(seconds=__TIME_OUT__)
@retry(
    max_attempts=__MAX_ATTEMPTS__,
    when=retry.when.raises(Exception),
    stop=retry.stop.after_attempt(__MAX_ATTEMPTS__) | retry.stop.after_delay(10),
    backoff=retry.backoff.jittered(multiplier=2),
)
@ratelimit(calls=__RATE_LIMIT_CALLS__, period=__RATE_LIMIT_PERIOD_CALLS__)
class RemoteSource(Consumer):

    @returns.from_json
    @raise_api_error
    @get("/v1/episodes")
    def get_episodes(
        self,
        headers: HeaderMap,
        mal_id: Query(name="malId", type=int),
        limit: Query(name="limit", type=int),
        after: Query(name="after", type=str),
        before: Query(name="before", type=str),
        kind: Query(name="kind", type=str),
        specials_only: Query(name="specialsOnly", type=bool),
        start: Query(name="start", type=int),
        end: Query(name="end", type=int),
        include_orphans: Query(name="includeOrphans", type=bool),
    ) -> EpisodesResponse:
        """Fetch paginated episodes for a MAL series"""
        pass

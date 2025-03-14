from typing import Mapping, Type
from marshmallow import EXCLUDE, Schema
from marshmallow_dataclass import class_schema
from uplink import (
    get,
    install,
    returns,
    timeout,
    retry,
    ratelimit,
    Consumer,
    HeaderMap,
    Query,
    loads,
    install,
)

from core.decorators import raise_api_error
from core import (
    __TIME_OUT__,
    __MAX_ATTEMPTS__,
    __RATE_LIMIT_CALLS__,
    __RATE_LIMIT_PERIOD_CALLS__,
)
from ..data.schemas import NewsConnectionSchema


@install
@loads.from_json(NewsConnectionSchema)
def load_model_from_json(
    model_type: Type[NewsConnectionSchema], json: Mapping[str, any]
) -> NewsConnectionSchema:
    schema: Type[Schema] = class_schema(model_type)()
    result = schema.load(json, unknown=EXCLUDE)
    return result


@timeout(seconds=5)
@retry(
    max_attempts=3,
    when=retry.when.raises(Exception),
    stop=retry.stop.after_attempt(3) | retry.stop.after_delay(2),
    backoff=retry.backoff.jittered(multiplier=2),
)
@ratelimit(calls=__RATE_LIMIT_CALLS__, period=__RATE_LIMIT_PERIOD_CALLS__)
class RemoteSource(Consumer):

    @returns.from_json
    @raise_api_error
    @get("news")
    def get_news(
        self,
        headers: HeaderMap,
        after: Query,
        before: Query,
        limit: Query,
    ) -> NewsConnectionSchema:
        """Fetch paginated news items using cursor-based pagination
        :param headers: Request headers
        :param after: Cursor for next page (ID of last item in current page)
        :param before: Cursor for previous page (ID of first item in current page)
        :param limit: Limit of results to fetch
        :return: NewsConnectionSchema
        """
        pass

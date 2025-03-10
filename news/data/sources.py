from typing import Optional
from marshmallow import EXCLUDE
from uplink import get, returns, timeout, retry, ratelimit, Consumer, HeaderMap, Query

from core.decorators import raise_api_error
from core import __TIME_OUT__, __MAX_ATTEMPTS__, __RATE_LIMIT_CALLS__, __RATE_LIMIT_PERIOD_CALLS__
from ..data.schemas import NewsConnectionSchema


@timeout(seconds=5)
@retry(
    max_attempts=3,
    when=retry.when.raises(Exception),
    stop=retry.stop.after_attempt(3) | retry.stop.after_delay(2),
    backoff=retry.backoff.jittered(multiplier=0.5)
)
@ratelimit(
    calls=__RATE_LIMIT_CALLS__,
    period=__RATE_LIMIT_PERIOD_CALLS__
)
class RemoteSource(Consumer):

    @returns(NewsConnectionSchema(unknown=EXCLUDE))
    @raise_api_error
    @get("news")
    def get_news(
        self, 
        headers: HeaderMap,
        after: Query,
        before: Query,
        limit: Query,
    ):
        """Fetch paginated news items using cursor-based pagination
        :param headers: Request headers
        :param after: Cursor for next page (ID of last item in current page)
        :param before: Cursor for previous page (ID of first item in current page)
        :param limit: Limit of results to fetch
        :return: NewsConnectionSchema
        """
        pass
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
    Path,
)

from core.decorators import raise_api_error
from core import (
    __TIME_OUT__,
    __MAX_ATTEMPTS__,
    __RATE_LIMIT_CALLS__,
    __RATE_LIMIT_PERIOD_CALLS__,
)
from ..data.schemas import MediaApiResponse


@install
@loads.from_json(MediaApiResponse)  # Adjusted for MediaApiResponse
def load_model_from_json(
    model_type: Type[MediaApiResponse], json: Mapping[str, any]
) -> MediaApiResponse:
    # Using marshmallow_dataclass to load directly into dataclass
    # This assumes the JSON keys match the dataclass field names
    schema = class_schema(model_type)()
    result = schema.load(json, unknown=EXCLUDE)  # EXCLUDE unknown fields
    return result


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
    @get("series")
    def get_series_by_id(
        self, series_id: Query(name="id", type=int), headers: HeaderMap  # type: ignore
    ) -> MediaApiResponse:
        """
        Fetches a series by its ID from the on-the-edge API.
        :param series_id: The ID of the series to fetch.
        :param headers: Request headers.
        :return: MediaEntity
        """
        pass

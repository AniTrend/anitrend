from typing import Mapping, Type, cast
from marshmallow import EXCLUDE
from marshmallow_dataclass import class_schema
from uplink import (
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
from ..data.schemas import ConfigurationSchema


@install
@loads.from_json(ConfigurationSchema)
def load_model_from_json(
    model_type: Type[ConfigurationSchema], json: Mapping[str, object]
) -> ConfigurationSchema:
    schema = class_schema(model_type)()
    result = schema.load(json, unknown=EXCLUDE)
    return cast(ConfigurationSchema, result)


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
    @get("/v1/config")
    def get_config(self, headers: HeaderMap) -> ConfigurationSchema:  # type: ignore
        """
        :return: ConfigurationSchema
        """
        pass

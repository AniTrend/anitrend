from marshmallow import EXCLUDE
from uplink import get, timeout, retry, ratelimit, Consumer, HeaderMap

from core.decorators import raise_api_error
from core import __TIME_OUT__, __MAX_ATTEMPTS__, __RATE_LIMIT_CALLS__, __RATE_LIMIT_PERIOD_CALLS__
from ..data.schemas import ConfigurationSchema


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

    @raise_api_error
    @get("config")
    def get_config(self, headers: HeaderMap) -> ConfigurationSchema(unknown=EXCLUDE):
        """
        :return: ConfigurationSchema
        """
        pass

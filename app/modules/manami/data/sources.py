from uplink import get, timeout, retry, ratelimit, Consumer
from marshmallow import EXCLUDE

from app.modules.common.decorators import raise_api_error
from ..data.schemas import Container

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
class RemoteSource(Consumer):

    @raise_api_error
    @get("master/anime-offline-database.json")
    def get_anime_entries(self) -> Container(unknown=EXCLUDE):
        """
        Retrieve a snapshot of relations
        :return: AnimeContainer
        """
        pass

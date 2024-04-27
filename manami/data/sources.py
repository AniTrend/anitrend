from marshmallow import EXCLUDE
from uplink import get, timeout, retry, ratelimit, Consumer

from core.decorators import raise_api_error
from core import __TIME_OUT__, __MAX_ATTEMPTS__, __RATE_LIMIT_CALLS__, __RATE_LIMIT_PERIOD_CALLS__
from ..data.schemas import Container


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

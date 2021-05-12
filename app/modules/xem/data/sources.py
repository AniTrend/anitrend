from uplink import get, timeout, retry, ratelimit, Consumer, Query
from .schemas import Container
from marshmallow import EXCLUDE
from app.modules.common.decorators import raise_api_error

__TIME_OUT__: int = 120
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
    @get("map/allNames")
    def get_all_names(
            self,
            origin: Query(name='origin', type=str),
            language: Query(name='language', type=str),
            default_names: Query(name='defaultNames', type=int)
    ) -> Container(unknown=EXCLUDE):
        """
        Retrieve all the names and id mappings for this listing
        :param origin: Non optional params: origin(an entity string like 'tvdb', 'anidb')
        :param language: A language string like 'us' or 'jp' default is all
        :param default_names: 1(yes) or 0(no) should the default names be added to the list ? default is 0(no)
        :return: XemContainer
        """
        pass

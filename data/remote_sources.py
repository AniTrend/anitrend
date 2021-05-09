from uplink import get, timeout, retry, ratelimit, Consumer, Query, error_handler
from data.model_schemas import XemContainer, RelationContainer
from marshmallow import EXCLUDE
from di import MainContainer

# 10 minutes read timeout
__TIME_OUT__: int = 600
__MAX_ATTEMPTS__: int = 5
__RATE_LIMIT_CALLS__: int = 5
__RATE_LIMIT_PERIOD_CALLS__: int = 10


@error_handler(requires_consumer=True)
def raise_api_error(exc_type, exc_val, exc_tb):
    logging_utility = MainContainer.logging_utility()
    logger = logging_utility.get_default_logger(__name__)
    logger.warning(f"API error occurred -> exc_type: {exc_type} exc_val: {exc_val} exc_tb: {exc_tb}")


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
class XemRemoteSource(Consumer):

    @raise_api_error
    @get("map/allNames")
    def get_all_names(
            self,
            origin: Query(name='origin', type=str),
            language: Query(name='language', type=str),
            default_names: Query(name='defaultNames', type=int)
    ) -> XemContainer(unknown=EXCLUDE):
        """
        Retrieve all the names and id mappings for this listing
        :param origin: Non optional params: origin(an entity string like 'tvdb', 'anidb')
        :param language: A language string like 'us' or 'jp' default is all
        :param default_names: 1(yes) or 0(no) should the default names be added to the list ? default is 0(no)
        :return:
        """
        pass


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
class RelationRemoteSource(Consumer):

    @raise_api_error
    @get("master/anime-offline-database.json")
    def get_anime_entries(self) -> RelationContainer(unknown=EXCLUDE):
        """
        Retrieve a snapshot of relations
        :return:
        """
        pass

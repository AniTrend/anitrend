import logging

from uplink import error_handler, timeout, retry, ratelimit

from . import (
    __MAX_ATTEMPTS__,
    __TIME_OUT__,
    __RATE_LIMIT_PERIOD_CALLS__,
    __RATE_LIMIT_CALLS__
)


@error_handler(requires_consumer=True)
def raise_api_error(exc_type=None, exc_val=None, exc_tb=None):
    logger = logging.getLogger("django")
    logger.warning(f"API error occurred -> exc_type: {exc_type} exc_val: {exc_val} exc_tb: {exc_tb}")


def retry_and_ratelimit_strategy(cls):
    """
    Assigns decorators for retry and ratelimit strategies for our uplink clients
    :param cls: Consumer class that will be decorated
    :return:
    """
    return timeout(seconds=__TIME_OUT__)(
        retry(
            max_attempts=__MAX_ATTEMPTS__,
            when=retry.when.raises(Exception),
            stop=(
                    retry.stop.after_attempt(__MAX_ATTEMPTS__)
                    | retry.stop.after_delay(__RATE_LIMIT_PERIOD_CALLS__)
            ),
            backoff=retry.backoff.jittered(multiplier=0.5),
        )(
            ratelimit(
                calls=__RATE_LIMIT_CALLS__,
                period=__RATE_LIMIT_PERIOD_CALLS__,
            )(cls)
        )
    )

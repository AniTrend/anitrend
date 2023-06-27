import logging

from dependency_injector import containers, providers
from growthbook import GrowthBook

from requests import Session
from core import LoggingUtility, TimeUtility
from django.conf import settings


def on_experiment_viewed(experiment, result):
    logging.getLogger("django")\
        .info(f"{experiment} viewed with result: {result}")


class AppContainer(containers.DeclarativeContainer):
    """Main application container"""

    config = providers.Configuration()

    session = providers.Factory(Session)

    logging_utility = providers.Singleton(
        LoggingUtility,
        is_debug=config.DEBUG,
    )

    time_zone_utility = providers.Singleton(
        TimeUtility,
        logger=logging_utility().get_default_logger(
            "utility.common.time_zone"
        ),
        time_zone=config.TIME_ZONE
    )

    growth_book = providers.Singleton(
        GrowthBook,
        api_host=settings.GROWTH_BOOK["host"],
        client_key=settings.GROWTH_BOOK["key"],
        cache_ttl=settings.GROWTH_BOOK["ttl"],
        trackingCallback=on_experiment_viewed
    )
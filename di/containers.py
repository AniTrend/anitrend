import logging

from dependency_injector import containers, providers
from django.conf import settings
from growthbook import GrowthBook
from requests import Session

from core import TimeUtility


def on_experiment_viewed(experiment, result):
    logging.getLogger("django") \
        .info(f"{experiment} viewed with result: {result}")


class CoreContainer(containers.DeclarativeContainer):
    """Main application container"""

    config = providers.Configuration()

    session = providers.Factory(Session)

    time_zone_utility = providers.Singleton(
        TimeUtility,
        time_zone=config.TIME_ZONE
    )

    growth_book = providers.Singleton(
        GrowthBook,
        api_host=settings.GROWTH_BOOK["host"],
        client_key=settings.GROWTH_BOOK["key"],
        cache_ttl=settings.GROWTH_BOOK["ttl"],
        trackingCallback=on_experiment_viewed
    )

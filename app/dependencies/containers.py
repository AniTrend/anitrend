from dependency_injector import containers, providers

from requests import Session
from ..modules.common import LoggingUtility, TimeUtility


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

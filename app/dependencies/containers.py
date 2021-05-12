from dependency_injector import containers, providers

from requests import Session
from ..modules.common import LoggingUtility


class AppContainer(containers.DeclarativeContainer):
    """Main application container"""

    config = providers.Configuration()

    session = providers.Factory(Session)

    logging_utility = providers.Singleton(
        LoggingUtility,
        is_debug=config.DEBUG,
    )

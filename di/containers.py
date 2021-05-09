from dependency_injector import containers, providers

from common import LoggingUtility


class MainContainer(containers.DeclarativeContainer):
    from django.conf import settings
    __cut_off_log_level = "DEBUG"
    if not settings.DEBUG:
        __cut_off_log_level = "INFO"

    logging_utility = providers.Singleton(
        LoggingUtility,
        log_level=__cut_off_log_level,
    )

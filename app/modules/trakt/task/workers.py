from time import sleep
from typing import Any, Optional

from app.dependencies import AppContainer


def start_sync_poll(*args, **kwargs) -> Optional[Any]:
    """
    Starts a worker or multiple workers
    """
    logging_utility = AppContainer.logging_utility()
    logger = logging_utility.get_default_logger(__name__)
    logger.info("Starting up workers")
    sleep(5)
    return f"{__name__} task finished after 5 seconds"

import logging
from time import sleep
from typing import Any, Optional


def start_sync_poll(*args, **kwargs) -> Optional[Any]:
    """
    Starts a worker or multiple workers
    """
    logger = logging.getLogger("django")
    logger.info("Starting up workers")
    sleep(5)
    return f"{__name__} task finished after 5 seconds"

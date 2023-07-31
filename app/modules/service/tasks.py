import logging
from time import sleep
from typing import Any, Optional


def start_workers(*args, **kwargs) -> Optional[Any]:
    """
    Starts a worker or multiple workers
    """
    logger = logging.getLogger("django")
    logger.info("Starting up workers")
    sleep(5)
    return "I am done :)"


def after_work_completed(*args, **kwargs) -> Optional[Any]:
    """
    Starts a worker or multiple workers
    """
    logger = logging.getLogger("django")
    logger.info("Starting after work completed")
    sleep(2)
    return "Work was ran and so was I :)"

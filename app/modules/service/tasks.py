from time import sleep
from typing import Any, Optional

from dependency_injector.wiring import inject, Provide


@inject
def start_workers(logging_utility=Provide["logging_utility"], *args, **kwargs) -> Optional[Any]:
    """
    Starts a worker or multiple workers
    """
    logging_utility.get_default_logger(__name__).info("Starting up workers")
    sleep(5)
    return "I am done :)"


@inject
def after_work_completed(logging_utility=Provide["logging_utility"], *args, **kwargs) -> Optional[Any]:
    """
    Starts a worker or multiple workers
    """
    logging_utility.get_default_logger(__name__).info("Starting after work completed")
    sleep(2)
    return "Work was ran and so was I :)"

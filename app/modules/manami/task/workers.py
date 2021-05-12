from typing import Any, Optional

from app.dependencies import AppContainer
from ..di import UseCaseContainer


def start_sync_poll(*args, **kwargs) -> Optional[Any]:
    """
    Starts a worker or multiple workers
    """
    logging_utility = AppContainer.logging_utility()
    logger = logging_utility.get_default_logger(__name__)
    logger.info("Poll task starting")
    return UseCaseContainer.use_case().fetch_all_records()

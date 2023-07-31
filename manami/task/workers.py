import logging
from typing import Any, Optional

from ..di import UseCaseContainer


def start_sync_poll(*args, **kwargs) -> Optional[Any]:
    """
    Starts a worker or multiple workers
    """
    logger = logging.getLogger("django")
    logger.info("Poll task starting")
    return UseCaseContainer.use_case().fetch_all_records()

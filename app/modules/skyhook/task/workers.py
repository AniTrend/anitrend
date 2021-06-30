from typing import Any, Optional

from app.dependencies import AppContainer
from ..di import UseCaseContainer


def find_show_by_id(*args, **kwargs) -> Optional[Any]:
    """
    Starts a worker or multiple workers
    """
    logging_utility = AppContainer.logging_utility()
    logger = logging_utility.get_default_logger(__name__)
    logger.info(f"Searching for show using args: {kwargs}")
    return UseCaseContainer.use_case().find_series_by_tvdb_id(kwargs)

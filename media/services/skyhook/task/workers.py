from typing import Any, Optional

from ..di import UseCaseContainer


def find_show_by_id(*args, **kwargs) -> Optional[Any]:
    """
    Starts a worker or multiple workers
    """
    logging.getLogger("django")
    logger = logging.getLogger("django")
    logger.info(f"Searching for show using args: {kwargs}")
    return UseCaseContainer.use_case().find_series_by_tvdb_id(kwargs)

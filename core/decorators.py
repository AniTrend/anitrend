import logging

from uplink import error_handler


@error_handler(requires_consumer=True)
def raise_api_error(consumer, exc_type=None, exc_val=None, exc_tb=None):
    logger = logging.getLogger("django")
    logger.warning(f"API error occurred -> exc_type: {exc_type} exc_val: {exc_val} exc_tb: {exc_tb}")

from uplink import error_handler
from app.dependencies import AppContainer


@error_handler(requires_consumer=True)
def raise_api_error(exc_type, exc_val, exc_tb):
    logging_utility = AppContainer.logging_utility()
    logger = logging_utility.get_default_logger(__name__)
    logger.warning(f"API error occurred -> exc_type: {exc_type} exc_val: {exc_val} exc_tb: {exc_tb}")


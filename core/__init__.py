"""Core graphql package"""
from .entities import AttributeDictionary
from .utilities import TimeUtility


__TIME_OUT__: int = 180
__MAX_ATTEMPTS__: int = 5
__RATE_LIMIT_CALLS__: int = 5
__RATE_LIMIT_PERIOD_CALLS__: int = 10


def str_to_enum(name):
    """Create an enum value from a string."""
    return name.replace(" ", "_").replace("-", "_").upper()

"""Core graphql package"""
from .utilities import LoggingUtility, TimeUtility
from .entities import AttributeDictionary


def str_to_enum(name):
    """Create an enum value from a string."""
    return name.replace(" ", "_").replace("-", "_").upper()

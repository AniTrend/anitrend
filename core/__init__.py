"""Core graphql package"""
from .entities import AttributeDictionary
from .utilities import TimeUtility


def str_to_enum(name):
    """Create an enum value from a string."""
    return name.replace(" ", "_").replace("-", "_").upper()

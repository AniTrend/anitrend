"""Core graphql package"""
from .helpers import Logging, FileSystem
from .utilities import LoggingUtility, TimeUtility
from .entities import AttributeDictionary


def str_to_enum(name):
    """Create an enum value from a string."""
    return name.replace(" ", "_").replace("-", "_").upper()

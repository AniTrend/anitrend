"""Main package"""
__version__ = "0.1.0"

from di import CoreContainer
from . import settings

container = CoreContainer()
container.config.from_dict(settings.__dict__)

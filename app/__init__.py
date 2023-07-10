"""Main package"""

from di import CoreContainer
from . import settings

container = CoreContainer()
container.config.from_dict(settings.__dict__)

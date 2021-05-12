"""Main package"""

from app.dependencies import AppContainer
from . import settings

container = AppContainer()
container.config.from_dict(settings.__dict__)

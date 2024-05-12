import logging
from typing import NoReturn

from dependency_injector.wiring import Provide, inject
from django.http import HttpRequest
from growthbook import GrowthBook

from di import CoreContainer


class LoggerMixin:

    def __init__(self) -> None:
        self._logger = logging.getLogger('django')


class GrowthBookMixin:

    @inject
    def __init__(self, growth_book=Provide[CoreContainer.growth_book]) -> None:
        self.__growth_book: GrowthBook = growth_book

    def process_request(
            self,
            request: HttpRequest,
    ) -> NoReturn:
        request.feature = self.__growth_book
        request.feature.load_features()

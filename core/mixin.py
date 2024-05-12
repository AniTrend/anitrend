import logging
from typing import NoReturn

from dependency_injector.wiring import Provide, inject
from django.http import HttpRequest, HttpResponse
from growthbook import GrowthBook

from core.models import ContextHeader
from di import CoreContainer


class LoggerMixin:

    def __init__(self) -> None:
        self._logger = logging.getLogger('django')


class GrowthBookMixin(LoggerMixin):

    @inject
    def __init__(self, growth_book=Provide[CoreContainer.growth_book]) -> None:
        super().__init__()
        self.__growth_book: GrowthBook = growth_book

    def set_request_attributes(self, context_header: ContextHeader):
        user_agent_info = context_header.user_agent_info
        application = context_header.application
        self.__growth_book.set_attributes({
            'app_locale': application.locale,
            'app_version': application.version,
            'app_source': application.source,
            'app_code': application.code,
            'app_name': application.label,
            'app_build_type': application.buildType,
            'browser_name': user_agent_info.user_agent.family,
            'browser_version': user_agent_info.user_agent.version,
            'cpu_architecture': user_agent_info.cpu.architecture,
            'device_model': user_agent_info.device.model,
            'device_vendor': user_agent_info.device.brand,
            'device_type': user_agent_info.device.family,
            'engine_name': user_agent_info.engine.family,
            'engine_version': user_agent_info.engine.version,
            'os_name': user_agent_info.os.family,
            'os_version': user_agent_info.os.version,
        })

    def process_request(self, request: HttpRequest) -> NoReturn:
        self._logger.info('loading growth_book features')
        self.__growth_book.load_features()
        if hasattr(request, 'context_header'):
            self.set_request_attributes(
                context_header=request.context_header
            )
        else:
            self._logger.warning('context_header is not defined in the current request context')
        request.feature = self.__growth_book

    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        self._logger.info('destroying growth_book instance')
        self.__growth_book.destroy()
        return response

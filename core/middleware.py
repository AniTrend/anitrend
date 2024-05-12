import logging
from typing import Optional, Dict

from django.http import HttpRequest, JsonResponse, HttpResponse
from django.utils.deprecation import MiddlewareMixin

from .mixin import GrowthBookMixin, LoggerMixin
from .models import ContextHeader, Application
from .utils import UAParser


class FeatureFlagMiddleware(MiddlewareMixin, GrowthBookMixin):
    pass


class HeaderMiddleware(MiddlewareMixin, LoggerMixin):

    def __fail(self, header: str) -> JsonResponse:
        response = JsonResponse(
            {
                'errors': [
                    {'message': 'Missing required header'}
                ]
            }
        )
        response.status_code = 400
        self._logger.error(f"Required header is missing from request: {header}")
        return response

    def process_request(
            self,
            request: HttpRequest,
    ) -> Optional[HttpResponse]:
        headers = request.META
        ua_parser = UAParser(user_agent=headers.get('HTTP_USER_AGENT'))

        request.context_header = ContextHeader(
            authorization=headers.get('HTTP_AUTHORIZATION'),
            accepts=headers.get('HTTP_ACCEPT'),
            content_type=headers.get('CONTENT_TYPE'),
            accept_encoding=headers.get('HTTP_ACCEPT_ENCODING'),
            application=Application(
                locale=headers.get('HTTP_X_APP_LOCALE'),
                version=headers.get('HTTP_X_APP_VERSION'),
                source=headers.get('HTTP_X_APP_SOURCE'),
                code=headers.get('HTTP_X_APP_CODE'),
                label=headers.get('HTTP_X_APP_NAME'),
                buildType=headers.get('HTTP_X_APP_BUILD_TYPE'),
            ),
            user_agent_info=ua_parser.get_result(),
        )

        enforced = [
            'HTTP_HOST',
            'HTTP_ACCEPT',
            'HTTP_ACCEPT_ENCODING',
            'HTTP_USER_AGENT',
        ]

        for header in enforced:
            if header not in headers:
                return self.__fail(header)

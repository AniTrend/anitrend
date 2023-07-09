from typing import Optional, Dict

from django.http import HttpRequest, JsonResponse, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from growthbook import GrowthBook
from rollbar.contrib.django.middleware import RollbarNotifierMiddleware

from .mixin import GrowthBookMixin, LoggerMixin
from .models import ContextHeader, Application


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

        request.context_header = ContextHeader(
            authorization=headers.get('HTTP_AUTHORIZATION'),
            accepts=headers.get('HTTP_ACCEPT'),
            agent=headers.get('HTTP_USER_AGENT'),
            contentType=headers.get('CONTENT_TYPE'),
            acceptEncoding=headers.get('HTTP_ACCEPT_ENCODING'),
            language=headers.get('HTTP_ACCEPT_LANGUAGE'),
            application=Application(
                locale=headers.get('HTTP_X_APP_LOCALE'),
                version=headers.get('HTTP_X_APP_VERSION'),
                source=headers.get('HTTP_X_APP_SOURCE'),
                code=headers.get('HTTP_X_APP_CODE'),
                label=headers.get('HTTP_X_APP_NAME'),
                buildType=headers.get('HTTP_X_APP_BUILD_TYPE'),
            )
        )

        enforced = [
            'HTTP_HOST',
            'HTTP_ACCEPT',
            'HTTP_ACCEPT_ENCODING',
            'HTTP_ACCEPT_LANGUAGE',
            'HTTP_USER_AGENT',
        ]

        for header in enforced:
            if header not in headers:
                return self.__fail(header)


class CustomRollbarNotifierMiddleware(RollbarNotifierMiddleware):

    def get_extra_data(self, request, exc) -> Dict:
        feature: GrowthBook = request.feature
        context: ContextHeader = request.context_header

        # Example of adding arbitrary metadata (optional)
        extra_data: Dict = {
            'user_agent': context.agent,
            'feature_flags': feature.get_features()
        }

        return extra_data

    def get_payload_data(self, request, exc) -> Dict:
        payload_data: Dict = dict()

        if not request.user.is_anonymous:
            # Adding info about the user affected by this event (optional)
            # The 'id' field is required, anything else is optional
            payload_data = {
                'person': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                },
            }

        return payload_data

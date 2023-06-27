import unittest

from django.http import JsonResponse
from django.test import RequestFactory

from app.header.models import ContextHeader
from .middleware import HeaderMiddleware


class HeaderMiddlewareTest(unittest.TestCase):

    def setUp(self) -> None:
        self.middleware = HeaderMiddleware(JsonResponse({'message': 'hello world'}))
        self.factory = RequestFactory()

    def test_process_request_with_headers(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer token',
            'HTTP_ACCEPT': 'application/json',
            'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                               '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'CONTENT_TYPE': 'application/json',
            'HTTP_ACCEPT_ENCODING': 'gzip, deflate',
            'HTTP_ACCEPT_LANGUAGE': 'en-US,en;q=0.9',
            'HTTP_X_APP_LOCALE': 'en-US',
            'HTTP_X_APP_VERSION': '1.0',
            'HTTP_X_APP_CODE': 'xyz123',
            'HTTP_X_APP_SOURCE': 'web',
            'HTTP_X_APP_NAME': 'MyApp',
            'HTTP_X_APP_BUILD_TYPE': 'release',
        }
        request = self.factory.get('/', **headers)
        self.middleware.process_request(request)

        context_header: ContextHeader = request.context_header

        self.assertEqual(context_header.authorization, 'Bearer token')
        self.assertEqual(context_header.accepts, 'application/json')
        self.assertEqual(context_header.agent, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                               ' (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
        self.assertEqual(context_header.contentType, 'application/json')
        self.assertEqual(context_header.acceptEncoding, 'gzip, deflate')
        self.assertEqual(context_header.language, 'en-US,en;q=0.9')
        # self.assertEqual(context_header.device.browser, 'Chrome')
        # self.assertEqual(context_header.device.cpu, None)
        # self.assertEqual(context_header.device.device, None)
        # self.assertEqual(context_header.device.engine, 'Chrome')
        # self.assertEqual(context_header.device.os, 'Windows NT 10.0')
        self.assertEqual(context_header.application.locale, 'en-US')
        self.assertEqual(context_header.application.version, '1.0')
        self.assertEqual(context_header.application.source, 'web')
        self.assertEqual(context_header.application.code, 'xyz123')
        self.assertEqual(context_header.application.label, 'MyApp')
        self.assertEqual(context_header.application.buildType, 'release')


if __name__ == '__main__':
    unittest.main()

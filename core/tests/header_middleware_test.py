import unittest
from datetime import datetime

from django.http import JsonResponse
from django.test import RequestFactory
import pytest

from core.entities import ContextHeader
from core.middleware import HeaderMiddleware


class HeaderMiddlewareTest(unittest.TestCase):

    def setUp(self) -> None:
        self.middleware = HeaderMiddleware(JsonResponse({"message": "hello world"}))
        self.factory = RequestFactory()

    @pytest.mark.integration
    def test_process_request_with_headers(self):
        headers = {
            "HTTP_AUTHORIZATION": "Bearer token",
            "HTTP_ACCEPT": "application/json",
            "HTTP_USER_AGENT": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, "
            "like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            "CONTENT_TYPE": "application/json",
            "HTTP_ACCEPT_ENCODING": "gzip, deflate",
            "HTTP_ACCEPT_LANGUAGE": "en-US,en;q=0.9",
            "HTTP_X_APP_LOCALE": "en-US",
            "HTTP_X_APP_VERSION": "1.0",
            "HTTP_X_APP_CODE": "xyz123",
            "HTTP_X_APP_SOURCE": "web",
            "HTTP_X_APP_NAME": "MyApp",
            "HTTP_X_APP_BUILD_TYPE": "release",
        }
        request = self.factory.get("/", **headers)
        self.middleware.process_request(request)

        context_header: ContextHeader = request.context_header

        self.assertEqual(context_header.authorization, "Bearer token")
        self.assertEqual(context_header.accepts, "application/json")
        self.assertEqual(
            context_header.user_agent_info.raw,
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0"
            " Mobile Safari/537.36",
        )
        self.assertEqual(context_header.content_type, "application/json")
        self.assertEqual(context_header.accept_encoding, "gzip, deflate")
        self.assertEqual(
            context_header.user_agent_info.user_agent.family, "Chrome Mobile"
        )
        self.assertEqual(context_header.user_agent_info.user_agent.major, "124")
        self.assertEqual(context_header.user_agent_info.user_agent.minor, "0")
        self.assertEqual(context_header.user_agent_info.user_agent.patch, "0")
        self.assertIsNone(context_header.user_agent_info.cpu.architecture)
        self.assertEqual(context_header.user_agent_info.device.family, "Nexus 5")
        self.assertEqual(context_header.user_agent_info.device.brand, "LG")
        self.assertEqual(context_header.user_agent_info.device.model, "Nexus 5")
        self.assertIsNone(context_header.user_agent_info.engine.family)
        self.assertEqual(context_header.user_agent_info.os.family, "Android")
        self.assertEqual(context_header.user_agent_info.os.major, "6")
        self.assertEqual(context_header.user_agent_info.os.minor, "0")
        self.assertIsNone(context_header.user_agent_info.os.patch)
        self.assertIsNone(context_header.user_agent_info.os.patch_minor)
        self.assertEqual(context_header.application.locale, "en-US")
        self.assertEqual(context_header.application.version, "1.0")
        self.assertEqual(context_header.application.source, "web")
        self.assertEqual(context_header.application.code, "xyz123")
        self.assertEqual(context_header.application.label, "MyApp")
        self.assertEqual(context_header.application.buildType, "release")

import unittest
from datetime import datetime
from typing import Final

from django.http import JsonResponse
from django.test import RequestFactory

from .models import ContextHeader
from .middleware import HeaderMiddleware
from .utilities import LinkUtility, TimeUtility


class RegexSearchTestCase(unittest.TestCase):

    def test_find_anilist_source_ids(self):
        anilist: Final[str] = "https://anilist.co/anime/1535"
        _id = LinkUtility.extract_id_if_matches([anilist], "anilist.co")
        self.assertEqual(_id, "1535")

    def test_find_anidb_source_ids(self):
        anidb: Final[str] = "https://anidb.net/anime/4563"
        _id = LinkUtility.extract_id_if_matches([anidb], "anidb.net")
        self.assertEqual(_id, "4563")

    def test_find_mal_source_ids(self):
        mal: Final[str] = "https://myanimelist.net/anime/1535"
        _id = LinkUtility.extract_id_if_matches([mal], "myanimelist.net")
        self.assertEqual(_id, "1535")

    def test_find_kitsu_source_ids(self):
        kitsu: Final[str] = "https://kitsu.io/anime/1376"
        _id = LinkUtility.extract_id_if_matches([kitsu], "kitsu.io")
        self.assertEqual(_id, "1376")

    def test_find_animeplanet_source_ids(self):
        animeplanet: Final[str] = "https://anime-planet.com/anime/death-note"
        _id = LinkUtility.extract_id_if_matches([animeplanet], "anime-planet.com")
        self.assertEqual(_id, "death-note")

    def test_find_notify_source_ids(self):
        notify: Final[str] = "https://notify.moe/anime/0-A-5Fimg"
        _id = LinkUtility.extract_id_if_matches([notify], "notify.moe")
        self.assertEqual(_id, "0-A-5Fimg")


class TimeUtilTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.time_util = TimeUtility(

            time_zone="Africa/Johannesburg"
        )

    def test_as_local_time(self):
        expected = datetime.strptime('2020-03-16T21:37:14+0200', '%Y-%m-%dT%H:%M:%S%z')
        result = self.time_util.as_local_time('2020-03-16T19:37:14+0000', '%Y-%m-%dT%H:%M:%S%z')
        self.assertEqual(expected.toordinal(), result.toordinal())


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

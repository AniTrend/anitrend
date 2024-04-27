import unittest

from graphene import Schema
from graphene.test import Client

from .fixtures import init_fixtures
from ..queries import ConfigQuery


class ConfigQueryTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        init_fixtures()

    def test_config_query(self):
        query = """
        {
            config {
                settings {
                    analyticsEnabled
                }
                image {
                    banner
                    poster
                    loading
                    error
                    info
                    default
                }
            }
        }
        """

        expected = {
            "data": {
                "config": {
                    "settings": {
                        "analyticsEnabled": False
                    },
                    "image": {
                        "banner": "https://anitrend.co/media/banner.png",
                        "poster": "https://anitrend.co/media/poster.png",
                        "loading": "https://anitrend.co/media/loading.png",
                        "error": "https://anitrend.co/media/error.png",
                        "info": "https://anitrend.co/media/info.png",
                        "default": "https://anitrend.co/media/default.png"
                    }
                }
            }
        }

        client = Client(Schema(query=ConfigQuery))
        result = client.execute(query)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()

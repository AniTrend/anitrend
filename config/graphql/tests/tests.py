import unittest

from graphene.test import Client
from graphene import Schema
from .fixtures import init_fixtures

from ..queries import ConfigQuery


class ConfigQueryTestCase(unittest.TestCase):
    def setUp(self) -> None:
        init_fixtures()

    def test_config_query(self):
        query = """
        {
            config {
                settings {
                    analyticsEnabled
                }
                defaultImage {
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

            }
        }

        client = Client(Schema(query=ConfigQuery))
        result = client.execute(query)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()

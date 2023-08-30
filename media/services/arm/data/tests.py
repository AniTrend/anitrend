import unittest
from unittest.mock import MagicMock

from .sources import ArmEndpoint


class TestSchemaSuite(unittest.TestCase):

    @unittest.skip('Not implemented yet')
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


class TestArmEndpoint(unittest.TestCase):

    def setUp(self):
        self.arm_endpoint = ArmEndpoint(base_url="https://arm.haglund.dev")

    def test_get_with_id(self):
        expected_response = {
            "anidb": 13945,
            "anilist": 101348,
            "anime-planet": "vinland-saga",
            "anisearch": 13486,
            "imdb": None,
            "kitsu": 41084,
            "livechart": 3169,
            "notify-moe": "Y3IK2Fiig",
            "themoviedb": None,
            "thetvdb": 359274,
            "myanimelist": 37521
        }

        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = expected_response
        self.arm_endpoint.get_with_id._execute_request = MagicMock(return_value=mock_response)

        response = self.arm_endpoint.get_with_id(id="101348", source="anilist")
        self.assertEqual(response, expected_response)

    def test_get_ids_from_tvdb(self):
        expected_response = [
            {
                "anidb": 13945,
                "anilist": 101348,
                "anime-planet": "vinland-saga",
                "anisearch": 13486,
                "imdb": None,
                "kitsu": 41084,
                "livechart": 3169,
                "notify-moe": "Y3IK2Fiig",
                "themoviedb": None,
                "thetvdb": 359274,
                "myanimelist": 37521
            },
            {
                "anidb": 16426,
                "anilist": 136430,
                "anime-planet": "vinland-saga-season-2",
                "anisearch": 16485,
                "imdb": None,
                "kitsu": 44875,
                "livechart": 10618,
                "notify-moe": "8BDBKMinR",
                "themoviedb": None,
                "thetvdb": 359274,
                "myanimelist": 49387
            }
        ]

        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = expected_response
        self.arm_endpoint.get_ids_from_tvdb._execute_request = MagicMock(return_value=mock_response)

        response = self.arm_endpoint.get_ids_from_tvdb(id="359274")
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()

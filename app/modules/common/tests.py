import unittest

from datetime import datetime
from typing import Final

from app.modules.common.utilities import LinkUtility, TimeUtility, LoggingUtility


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
        logging_utility = LoggingUtility(is_debug=True)
        self.time_util = TimeUtility(
            logger=logging_utility.get_default_logger("utility.common.time_zone"),
            time_zone="Africa/Johannesburg"
        )

    def test_as_local_time(self):
        expected = datetime.strptime('2020-03-16T21:37:14+0200', '%Y-%m-%dT%H:%M:%S%z')
        result = self.time_util.as_local_time('2020-03-16T19:37:14+0000', '%Y-%m-%dT%H:%M:%S%z')
        self.assertEqual(expected.toordinal(), result.toordinal())


if __name__ == '__main__':
    unittest.main()

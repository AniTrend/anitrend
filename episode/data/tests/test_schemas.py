import json
import unittest

from marshmallow_dataclass import class_schema

from core.helpers import FileSystem
from episode.data.schemas import Episode, EpisodesResponse, EpisodeThemes, EpisodeTitle


class TestEpisodeSchemas(unittest.TestCase):
    def setUp(self):
        fixture_content = FileSystem.get_file_contents("fixtures/edge", "episodes.json")
        self.fixture = json.loads(fixture_content)

    def test_episodes_response_schema(self):
        schema = class_schema(EpisodesResponse)()
        result = schema.load(self.fixture)

        self.assertEqual(result.count, self.fixture["count"])
        self.assertEqual(result.total, self.fixture["total"])
        self.assertEqual(result.first, self.fixture["first"])
        self.assertEqual(result.last, self.fixture["last"])
        self.assertIsInstance(result.data, list)
        self.assertEqual(len(result.data), len(self.fixture["data"]))

    def test_episode_schema_fields(self):
        schema = class_schema(Episode)()
        episode_data = self.fixture["data"][0]
        result = schema.load(episode_data)

        self.assertEqual(result.id, episode_data["id"])
        self.assertEqual(result.number, episode_data["number"])
        self.assertIsInstance(result.title, EpisodeTitle)
        self.assertEqual(result.title.english, episode_data["title"]["english"])
        self.assertEqual(result.synopsis, episode_data["synopsis"])
        self.assertEqual(result.aired, episode_data["aired"])
        self.assertEqual(result.score, episode_data["score"])
        self.assertEqual(result.kind, episode_data["kind"])
        self.assertEqual(result.duration, episode_data["duration"])
        self.assertEqual(result.url, episode_data["url"])
        self.assertEqual(result.tvdbShowId, episode_data["tvdbShowId"])
        self.assertEqual(result.tvdbId, episode_data["tvdbId"])
        self.assertEqual(result.tmdbId, episode_data["tmdbId"])
        self.assertEqual(result.seasonNumber, episode_data["seasonNumber"])
        self.assertEqual(result.episodeNumber, episode_data["episodeNumber"])
        self.assertEqual(
            result.absoluteEpisodeNumber, episode_data["absoluteEpisodeNumber"]
        )
        self.assertEqual(
            result.airedBeforeSeasonNumber, episode_data["airedBeforeSeasonNumber"]
        )
        self.assertEqual(
            result.airedBeforeEpisodeNumber, episode_data["airedBeforeEpisodeNumber"]
        )
        self.assertEqual(
            result.airedAfterSeasonNumber, episode_data["airedAfterSeasonNumber"]
        )
        self.assertEqual(
            result.airedAfterEpisodeNumber, episode_data["airedAfterEpisodeNumber"]
        )
        self.assertEqual(result.image, episode_data["image"])
        self.assertEqual(result.poster, episode_data["poster"])
        self.assertIsInstance(result.themes, EpisodeThemes)
        self.assertEqual(result.themes.openings, episode_data["themes"]["openings"])
        self.assertEqual(result.themes.endings, episode_data["themes"]["endings"])

    def test_episode_schema_optional_fields(self):
        schema = class_schema(Episode)()
        episode_data = self.fixture["data"][1]
        result = schema.load(episode_data)

        self.assertEqual(result.synopsis, episode_data["synopsis"])
        self.assertIsNone(result.aired)
        self.assertIsNone(result.score)
        self.assertEqual(result.kind, episode_data["kind"])
        self.assertEqual(result.tvdbShowId, episode_data["tvdbShowId"])
        self.assertEqual(result.image, episode_data["image"])
        self.assertEqual(result.poster, episode_data["poster"])
        self.assertEqual(result.themes.openings, [])
        self.assertEqual(result.themes.endings, ["Quiet Ending"])

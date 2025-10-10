import json
import unittest
from typing import cast

import pytest
from marshmallow import ValidationError
from marshmallow_dataclass import class_schema

from core.helpers import FileSystem
from media.data.schemas import (
    AnimeTheme,
    AnimeThemeMeta,
    MediaEntity,
    SeriesCoverImage,
    SeriesId,
    SeriesImageAttributes,
    SeriesNetwork,
    SeriesSchedule,
    SeriesScheduleEpisode,
    SeriesTitle,
    SeriesTrailer,
)


class TestMediaSchemas(unittest.TestCase):
    def setUp(self):
        full_fixture = json.loads(
            FileSystem.get_file_contents("fixtures/edge", "media.json")
        )
        self.data = full_fixture.get("data", {})
        if not self.data:
            raise ValueError(
                "Could not find 'data' in media.json fixture data. Please check fixture structure."
            )

    @pytest.mark.unit
    def test_media_loading_from_fixture(self):
        MediaEntitySchema = class_schema(MediaEntity)()
        try:
            media_instance = MediaEntitySchema.load(self.data)
        except Exception as e:
            self.fail(f"Failed to load Media from prepared fixture data: {e}")

        self.assertIsInstance(media_instance, MediaEntity)

    @pytest.mark.unit
    def test_individual_series_id_schema(self):
        SeriesIdSchema = class_schema(SeriesId)()
        result = cast(SeriesId, SeriesIdSchema.load(self.data["mediaId"]))
        self.assertEqual(result.anilist, 21699)
        self.assertEqual(result.myanimelist, 32937)
        self.assertEqual(result.anidb, 11992)
        self.assertEqual(
            result.slug, "konosuba-gods-blessing-on-this-wonderful-world-2"
        )

    @pytest.mark.unit
    def test_individual_series_title_schema(self):
        SeriesTitleSchema = class_schema(SeriesTitle)()
        result = cast(SeriesTitle, SeriesTitleSchema.load(self.data["title"]))
        self.assertEqual(result.romaji, "Kono Subarashii Sekai ni Shukufuku wo! 2")
        self.assertEqual(
            result.english, "KonoSuba: God's Blessing on This Wonderful World! 2"
        )
        self.assertEqual(result.japanese, "この素晴らしい世界に祝福を！ 2")

    @pytest.mark.unit
    def test_individual_cover_image_schema(self):
        CoverImageSchema = class_schema(SeriesCoverImage)()
        result = cast(SeriesCoverImage, CoverImageSchema.load(self.data["cover"]))
        self.assertEqual(result.color, "#020202")
        self.assertEqual(
            result.extraLarge,
            "https://cdn.myanimelist.net/images/anime/2/83188l.jpg",
        )
        self.assertEqual(
            result.large, "https://cdn.myanimelist.net/images/anime/2/83188l.jpg"
        )
        self.assertEqual(
            result.medium, "https://cdn.myanimelist.net/images/anime/2/83188t.jpg"
        )

    @pytest.mark.unit
    def test_individual_trailer_schema(self):
        TrailerSchema = class_schema(SeriesTrailer)()
        # Test with the first trailer in the fixture
        trailer_data = self.data["trailers"][0]
        result = cast(SeriesTrailer, TrailerSchema.load(trailer_data))
        self.assertEqual(result.id, "https://www.youtube.com/watch?v=9jVxMt845AY")
        self.assertEqual(result.site, "youtube")
        self.assertEqual(
            result.thumbnail, "https://img.youtube.com/vi/9jVxMt845AY/maxresdefault.jpg"
        )

    @pytest.mark.unit
    def test_individual_network_schema(self):
        NetworkSchema = class_schema(SeriesNetwork)()
        # Test with the first network in the fixture
        network_data = self.data["networks"][0]
        result = cast(SeriesNetwork, NetworkSchema.load(network_data))
        self.assertEqual(result.id, 614)
        self.assertEqual(
            result.logoPath,
            "https://image.tmdb.org/t/p/original/hSdroyVthq3CynxTIIY7lnS8w1.png",
        )
        self.assertEqual(result.name, "Tokyo MX")
        self.assertEqual(result.originCountry, "JP")
        self.assertTrue(result.isPrimary)
        self.assertEqual(result.category, "DISTRIBUTION")

    @pytest.mark.unit
    def test_individual_image_schema(self):
        ImageAttributeSchema = class_schema(SeriesImageAttributes)()
        first_image = cast(
            SeriesImageAttributes, ImageAttributeSchema.load(self.data["images"][0])
        )
        self.assertEqual(
            first_image.url,
            "https://image.tmdb.org/t/p/original/rvZJxD36tKoglL8fXoMMWKGQfM.jpg",
        )
        self.assertEqual(first_image.type, "BACKDROP")
        self.assertEqual(first_image.height, 2160)
        self.assertEqual(first_image.width, 3840)

    @pytest.mark.unit
    def test_individual_schedule_schema(self):
        ScheduleSchema = class_schema(SeriesSchedule)()
        schedule_data = self.data["schedule"]

        test_schedule_data = json.loads(json.dumps(schedule_data))
        if test_schedule_data.get("firstAirDate") is not None:
            test_schedule_data["firstAirDate"] = str(test_schedule_data["firstAirDate"])
        if test_schedule_data.get("lastAirDate") is not None:
            test_schedule_data["lastAirDate"] = str(test_schedule_data["lastAirDate"])

        if (
            test_schedule_data.get("lastAiredEpisode")
            and test_schedule_data["lastAiredEpisode"].get("airDate") is not None
        ):
            test_schedule_data["lastAiredEpisode"]["airDate"] = str(
                test_schedule_data["lastAiredEpisode"]["airDate"]
            )

        if (
            test_schedule_data.get("nextEpisodeToAir")
            and test_schedule_data["nextEpisodeToAir"].get("airDate") is not None
        ):
            test_schedule_data["nextEpisodeToAir"]["airDate"] = str(
                test_schedule_data["nextEpisodeToAir"]["airDate"]
            )

        result = cast(SeriesSchedule, ScheduleSchema.load(test_schedule_data))
        self.assertEqual(result.firstAirDate, 1452729600)
        self.assertEqual(result.lastAirDate, 1746576000)
        self.assertIsInstance(result.lastAiredEpisode, SeriesScheduleEpisode)
        self.assertIsNotNone(result.nextEpisodeToAir)
        if result.nextEpisodeToAir:
            self.assertEqual(result.nextEpisodeToAir.episodeNumber, 14)

    @pytest.mark.unit
    def test_individual_schedule_episode_schema(self):
        ScheduleEpisodeSchema = class_schema(SeriesScheduleEpisode)()
        schedule_episode_data = self.data["schedule"]["lastAiredEpisode"]

        test_schedule_episode_data = json.loads(json.dumps(schedule_episode_data))
        if test_schedule_episode_data.get("airDate") is not None:
            test_schedule_episode_data["airDate"] = str(
                test_schedule_episode_data["airDate"]
            )

        result = cast(
            SeriesScheduleEpisode,
            ScheduleEpisodeSchema.load(test_schedule_episode_data),
        )
        self.assertEqual(result.id, 6243441)
        self.assertEqual(result.name, "Episode 13")
        self.assertEqual(result.airDate, 1746576000)
        self.assertEqual(result.episodeNumber, 13)
        self.assertEqual(result.seasonNumber, 3)
        self.assertIsNone(result.image)
        self.assertEqual(result.tmdbId, 65844)

    @pytest.mark.unit
    def test_schedule_episode_missing_required_field_raises(self):
        ScheduleEpisodeSchema = class_schema(SeriesScheduleEpisode)()
        invalid_payload = json.loads(
            json.dumps(self.data["schedule"]["lastAiredEpisode"])
        )
        invalid_payload.pop("name", None)
        with pytest.raises(ValidationError):
            ScheduleEpisodeSchema.load(invalid_payload)

    @pytest.mark.unit
    def test_individual_anime_theme_schema(self):
        if not self.data.get("themeSongs"):
            self.skipTest("No theme songs data in fixture")
        AnimeThemeSchema = class_schema(AnimeTheme)()
        theme_data = self.data["themeSongs"][0]
        result = cast(AnimeTheme, AnimeThemeSchema.load(theme_data))
        self.assertEqual(result.id, "OP")
        self.assertIsInstance(result.meta, AnimeThemeMeta)
        self.assertEqual(result.meta.number, 1)
        self.assertEqual(result.meta.type, "OP")
        self.assertEqual(result.meta.version, 1)

    @pytest.mark.unit
    def test_media_entity_normalizes_optional_lists(self):
        MediaEntitySchema = class_schema(MediaEntity)()
        payload = json.loads(json.dumps(self.data))
        payload["images"] = None
        payload["themeSongs"] = None
        payload["trailers"] = None
        payload["networks"] = None

        media_instance = MediaEntitySchema.load(payload)

        self.assertEqual(media_instance.images, [])
        self.assertEqual(media_instance.themeSongs, [])
        self.assertEqual(media_instance.trailers, [])
        self.assertEqual(media_instance.networks, [])

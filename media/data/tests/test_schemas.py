import json
import unittest
import pytest
from marshmallow_dataclass import class_schema
from typing import cast

from core.helpers import FileSystem
from media.data.schemas import (
    AnimeTheme,
    AnimeThemeMeta,
    Media,
    SeriesCoverImage,
    SeriesEpisode,
    SeriesId,
    SeriesImage,
    SeriesImageBackdrop,
    SeriesNetwork,
    SeriesSchedule,
    SeriesScheduleEpisode,
    SeriesSeason,
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
                "Could not find 'mediaId' in media.json fixture data. Please check fixture structure."
            )

    @pytest.mark.unit
    def test_media_loading_from_fixture(self):
        MediaEntitySchema = class_schema(Media)()
        try:
            media_instance = MediaEntitySchema.load(self.data)
        except Exception as e:
            self.fail(f"Failed to load Media from prepared fixture data: {e}")

        self.assertIsInstance(media_instance, Media)

    @pytest.mark.unit
    def test_individual_episode_schema(self):
        EpisodeSchema = class_schema(SeriesEpisode)()
        result = cast(
            SeriesEpisode, EpisodeSchema.load(self.data["seasons"][0]["episodes"][0])
        )
        self.assertEqual(result.id, 1174618)
        self.assertEqual(result.tvdbShowId, 303867)
        self.assertEqual(result.tvdbId, 5463421)
        self.assertEqual(result.seasonNumber, 0)
        self.assertEqual(result.episodeNumber, 3)
        self.assertEqual(
            result.title,
            "God's Blessings on This Wonderful Choker!",
        )
        self.assertEqual(result.airDate, 1466778600)
        self.assertGreater(len(result.crew), 0)
        self.assertGreater(len(result.guests), 0)

    @pytest.mark.unit
    def test_individual_season_schema(self):
        SeasonSchema = class_schema(SeriesSeason)()
        result = cast(SeriesSeason, SeasonSchema.load(self.data["seasons"][0]))
        self.assertEqual(result.tmdbId, 75215)
        self.assertEqual(result.airDate, 1466726400)
        self.assertEqual(result.name, "Specials")
        self.assertEqual(result.episodeCount, 4)
        self.assertEqual(result.number, 0)
        self.assertEqual(
            result.cover,
            "https://image.tmdb.org/t/p/original/gfzUCmPA5PRhZtFV6FuHIF6eNTH.jpg",
        )

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
        ImageSchema = class_schema(SeriesImage)()
        image_data = self.data["image"]
        result = cast(SeriesImage, ImageSchema.load(image_data))
        self.assertIsInstance(result.backdrops, list)
        self.assertIsInstance(result.posters, list)
        self.assertIsInstance(result.logos, list)
        if result.backdrops:
            self.assertIsInstance(result.backdrops[0], SeriesImageBackdrop)
            self.assertEqual(result.backdrops[0].height, 2160)  # Example assertion
        if result.posters:
            self.assertIsInstance(result.posters[0], SeriesImageBackdrop)
            self.assertEqual(result.posters[0].width, 2000)  # Example assertion
        if result.logos:
            self.assertIsInstance(result.logos[0], SeriesImageBackdrop)
            self.assertEqual(result.logos[0].height, 189)  # Example assertion

    @pytest.mark.unit
    def test_individual_image_backdrop_schema(self):
        ImageBackdropSchema = class_schema(SeriesImageBackdrop)()
        # Test with the first backdrop in the fixture
        backdrop_data = self.data["image"]["backdrops"][0]
        result = cast(SeriesImageBackdrop, ImageBackdropSchema.load(backdrop_data))
        self.assertEqual(result.height, 2160)
        self.assertEqual(result.width, 3840)
        self.assertEqual(
            result.url,
            "https://image.tmdb.org/t/p/original/rvZJxD36tKoglL8fXoMMWKGQfM.jpg",
        )
        self.assertIsNone(result.locale)  # As per fixture

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
        self.assertIsNone(result.nextEpisodeToAir)

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

import json
import unittest

from marshmallow_dataclass import class_schema
import pytest
from core.helpers import FileSystem
from config.data.schemas import (
    ConfigurationSchema,
    SettingsSchema,
    ImageSchema,
    NavigationSchema,
    NavigationGroupSchema,
    GenreSchema,
)


class TestConfigSchemas(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(
            FileSystem.get_file_contents("fixtures/edge", "config.json")
        )

    @pytest.mark.unit
    def test_settings_schema(self):
        schema = class_schema(SettingsSchema)()
        settings_data = self.data["settings"]
        result = schema.load(settings_data)
        self.assertEqual(result.analyticsEnabled, settings_data["analyticsEnabled"])
        self.assertEqual(result.platformSource, settings_data.get("platformSource"))

    @pytest.mark.unit
    def test_image_schema(self):
        schema = class_schema(ImageSchema)()
        image_data = self.data["image"]
        result = schema.load(image_data)
        self.assertEqual(result.banner, image_data["banner"])
        self.assertEqual(result.poster, image_data["poster"])
        self.assertEqual(result.loading, image_data["loading"])
        self.assertEqual(result.error, image_data["error"])
        self.assertEqual(result.info, image_data["info"])
        self.assertEqual(result.default, image_data["default"])

    @pytest.mark.unit
    def test_navigation_group_schema(self):
        schema = class_schema(NavigationGroupSchema)()
        group_data = self.data["navigation"][0]["group"]
        result = schema.load(group_data)
        self.assertEqual(result.authenticated, group_data["authenticated"])
        self.assertEqual(result.i18n, group_data["i18n"])

    @pytest.mark.unit
    def test_navigation_schema(self):
        schema = class_schema(NavigationSchema)()
        nav_data = self.data["navigation"][0]
        result = schema.load(nav_data)
        self.assertEqual(result.criteria, nav_data["criteria"])
        self.assertEqual(result.destination, nav_data["destination"])
        self.assertEqual(result.i18n, nav_data["i18n"])
        self.assertEqual(result.icon, nav_data["icon"])
        self.assertEqual(result.group.authenticated, nav_data["group"]["authenticated"])
        self.assertEqual(result.group.i18n, nav_data["group"]["i18n"])

    @pytest.mark.unit
    def test_genre_schema(self):
        schema = class_schema(GenreSchema)()
        genre_data = self.data["genres"][0]
        result = schema.load(genre_data)
        self.assertEqual(result.name, genre_data["name"])
        self.assertEqual(result.mediaId, genre_data["mediaId"])

    @pytest.mark.unit
    def test_configuration_schema(self):
        schema = class_schema(ConfigurationSchema)()
        result = schema.load(self.data)
        self.assertEqual(result.id, self.data["id"])

        # Test settings
        self.assertEqual(
            result.settings.analyticsEnabled, self.data["settings"]["analyticsEnabled"]
        )
        self.assertEqual(
            result.settings.platformSource, self.data["settings"].get("platformSource")
        )

        # Test image if present
        if self.data.get("image"):
            self.assertEqual(result.image.banner, self.data["image"]["banner"])
            self.assertEqual(result.image.poster, self.data["image"]["poster"])
        else:
            self.assertIsNone(result.image)

        # Test navigation if present
        if self.data.get("navigation"):
            self.assertGreater(len(result.navigation), 0)
            nav = result.navigation[0]
            nav_data = self.data["navigation"][0]
            self.assertEqual(nav.criteria, nav_data["criteria"])
            self.assertEqual(nav.destination, nav_data["destination"])
        else:
            self.assertIsNone(result.navigation)

        # Test genres if present
        if self.data.get("genres"):
            self.assertGreater(len(result.genres), 0)
            genre = result.genres[0]
            genre_data = self.data["genres"][0]
            self.assertEqual(genre.name, genre_data["name"])
            self.assertEqual(genre.mediaId, genre_data["mediaId"])
        else:
            self.assertIsNone(result.genres)

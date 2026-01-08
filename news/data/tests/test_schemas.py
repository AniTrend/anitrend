import json
import unittest

from marshmallow_dataclass import class_schema
import pytest

from core.helpers import FileSystem
from news.data.schemas import NewsSchema, NewsConnectionSchema


class TestSchemas(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(
            FileSystem.get_file_contents("fixtures/edge", "news.json")
        )

    @pytest.mark.unit
    def test_news_schema(self):
        schema = class_schema(NewsSchema)()
        result = schema.load(self.data["data"][0])
        self.assertEqual(result.id, self.data["data"][0]["id"])
        self.assertEqual(result.title, self.data["data"][0]["title"])
        self.assertEqual(result.author, self.data["data"][0]["author"])
        self.assertEqual(result.description, self.data["data"][0]["description"])
        self.assertEqual(result.content, self.data["data"][0]["content"])
        self.assertEqual(result.image, self.data["data"][0]["image"])
        self.assertEqual(result.publishedOn, self.data["data"][0]["publishedOn"])
        self.assertEqual(result.link, self.data["data"][0]["link"])
        self.assertIsNone(result.category)
        self.assertIsNone(result.genre)
        self.assertIsNone(result.area)
        self.assertIsNone(result.lang)

    @pytest.mark.unit
    def test_news_connection_schema(self):
        schema = class_schema(NewsConnectionSchema)()
        result = schema.load(self.data)
        self.assertEqual(result.count, self.data["count"])
        self.assertEqual(result.first, self.data["first"])
        self.assertEqual(result.last, self.data["last"])
        self.assertIsInstance(result.data, list)
        self.assertEqual(len(result.data), len(self.data["data"]))

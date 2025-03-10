import json
import unittest

from core.helpers import FileSystem
from news.data.schemas import NewsSchema, NewsConnectionSchema


class TestSchemas(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(FileSystem.get_file_contents("fixtures/edge", "news.json"))

    def test_news_schema(self):
        schema = NewsSchema()
        result = schema.load(self.data["data"][0])
        self.assertEqual(result["id"], self.data["data"][0]["id"])
        self.assertEqual(result["title"], self.data["data"][0]["title"])
        self.assertEqual(result["author"], self.data["data"][0]["author"])
        self.assertEqual(result["description"], self.data["data"][0]["description"])
        self.assertEqual(result["content"], self.data["data"][0]["content"])
        self.assertEqual(result["image"], self.data["data"][0]["image"])
        self.assertEqual(result["published_on"], self.data["data"][0]["publishedOn"])
        self.assertEqual(result["link"], self.data["data"][0]["link"])

    def test_news_connection_schema(self):
        schema = NewsConnectionSchema()
        result = schema.load(self.data)
        self.assertEqual(result.count, self.data["count"])
        self.assertEqual(result.first, self.data["first"])
        self.assertEqual(result.last, self.data["last"])
        self.assertIsInstance(result.data, list)
        self.assertEqual(len(result.data), len(self.data["data"]))
import unittest
from unittest.mock import Mock, patch
from json import JSONDecodeError

import pytest

from news.data.repositories import NewsRepository
from news.data.schemas import NewsConnectionSchema, NewsSchema
from news.data.sources import RemoteSource


class TestNewsRepository(unittest.TestCase):
    def setUp(self):
        self.mock_remote_source = Mock(spec=RemoteSource)
        self.repository = NewsRepository(remote_source=self.mock_remote_source)
        self.test_headers = {"Authorization": "Bearer test"}
        self.test_after = "after_cursor"
        self.test_before = "before_cursor"
        self.test_limit = 10

        self.sample_news = NewsConnectionSchema(
            count=1,
            first="first_id",
            last="last_id",
            data=[
                NewsSchema(
                    id="test_id",
                    title="Test Title",
                    author="Test Author",
                    description="Test Description",
                    content="Test Content",
                    image="test.jpg",
                    publishedOn=1234567890,
                    link="https://test.com",
                )
            ],
        )

    @pytest.mark.integration
    def test_invoke_success(self):
        self.mock_remote_source.get_news.return_value = self.sample_news

        result = self.repository.invoke(
            headers=self.test_headers,
            after=self.test_after,
            before=self.test_before,
            limit=self.test_limit,
        )

        self.assertEqual(result, self.sample_news)
        self.mock_remote_source.get_news.assert_called_once_with(
            headers=self.test_headers,
            after=self.test_after,
            before=self.test_before,
            limit=self.test_limit,
        )

    @pytest.mark.integration
    def test_invoke_handles_json_decode_error(self):
        json_error = JSONDecodeError("Invalid JSON", "test", 0)
        self.mock_remote_source.get_news.side_effect = json_error

        with self.assertRaises(JSONDecodeError):
            self.repository.invoke(
                headers=self.test_headers,
                after=self.test_after,
                before=self.test_before,
                limit=self.test_limit,
            )

        self.mock_remote_source.get_news.assert_called_once_with(
            headers=self.test_headers,
            after=self.test_after,
            before=self.test_before,
            limit=self.test_limit,
        )

    @pytest.mark.integration
    def test_fetch_feed_success(self):
        feed_payload = [
            {
                "id": "feed_id",
                "title": "Feed Title",
                "author": "Feed Author",
                "description": "Feed Description",
                "content": "Feed Content",
                "image": "feed.jpg",
                "publishedOn": 1234567890,
                "link": "https://feed.test",
                "category": "Category",
                "genre": "Genre",
                "area": "Area",
                "lang": "en",
            }
        ]

        self.mock_remote_source.get_news_feed.return_value = feed_payload

        result = self.repository.fetch_feed(headers=self.test_headers, locale="en-US")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, feed_payload[0]["id"])
        self.mock_remote_source.get_news_feed.assert_called_once_with(
            headers=self.test_headers, locale="en-US"
        )

    @pytest.mark.integration
    def test_fetch_feed_handles_error(self):
        test_error = Exception("feed failure")
        self.mock_remote_source.get_news_feed.side_effect = test_error

        with self.assertRaises(Exception):
            self.repository.fetch_feed(headers=self.test_headers, locale=None)

        self.mock_remote_source.get_news_feed.assert_called_once_with(
            headers=self.test_headers, locale=None
        )

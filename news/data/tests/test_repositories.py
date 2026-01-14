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
                    link="https://test.com",
                    description="Test Description",
                    content="Test Content",
                    publishedOn=1234567890,
                    category="general",
                    genre="anime",
                    area="JP",
                    lang="en-US",
                    image="https://test.com/image.jpg",
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

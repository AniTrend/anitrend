import unittest
from unittest.mock import Mock, patch
from json import JSONDecodeError

from uplink import Consumer
from news.data.repositories import NewsRepository
from news.data.sources import RemoteSource
from news.domain.entities import NewsModel, NewsConnectionModel


class TestNewsRepository(unittest.TestCase):
    def setUp(self):
        self.mock_remote_source = Mock(spec=RemoteSource)
        self.repository = NewsRepository(remote_source=self.mock_remote_source)
        self.test_headers = {"Authorization": "Bearer test"}
        self.test_after = "after_cursor"
        self.test_before = "before_cursor"
        self.test_limit = 10
        
        self.sample_news = NewsConnectionModel(
            count=1,
            first="first_id",
            last="last_id",
            data=[
                NewsModel(
                    id="test_id",
                    title="Test Title",
                    author="Test Author",
                    description="Test Description",
                    content="Test Content",
                    image="test.jpg",
                    published_on=1234567890,
                    link="https://test.com"
                )
            ]
        )

    def test_invoke_success(self):
        # Arrange
        self.mock_remote_source.get_news.return_value = self.sample_news

        # Act
        result = self.repository.invoke(
            headers=self.test_headers,
            after=self.test_after,
            before=self.test_before,
            limit=self.test_limit
        )

        # Assert
        self.assertEqual(result, self.sample_news)
        self.mock_remote_source.get_news.assert_called_once_with(
            headers=self.test_headers,
            after=self.test_after,
            before=self.test_before,
            limit=self.test_limit
        )

    def test_invoke_handles_json_decode_error(self):
        # Arrange
        json_error = JSONDecodeError("Invalid JSON", "test", 0)
        self.mock_remote_source.get_news.side_effect = json_error

        # Act & Assert
        with self.assertRaises(JSONDecodeError):
            self.repository.invoke(
                headers=self.test_headers,
                after=self.test_after,
                before=self.test_before,
                limit=self.test_limit
            )

        self.mock_remote_source.get_news.assert_called_once_with(
            headers=self.test_headers,
            after=self.test_after,
            before=self.test_before,
            limit=self.test_limit
        )
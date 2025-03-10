import unittest
from unittest.mock import Mock, patch
from json import JSONDecodeError

from news.data.repositories import NewsRepository
from news.domain.usecases import NewsUseCase
from news.domain.entities import NewsModel, NewsConnectionModel


class TestNewsUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repository = Mock(spec=NewsRepository)
        self.use_case = NewsUseCase(repository=self.mock_repository)
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

    def test_fetch_news_success(self):
        # Arrange
        self.mock_repository.invoke.return_value = self.sample_news

        # Act
        result = self.use_case.fetch_news_connection(
            headers=self.test_headers,
            after=self.test_after,
            before=self.test_before,
            limit=self.test_limit
        )

        # Assert
        self.assertEqual(result, self.sample_news)
        self.mock_repository.invoke.assert_called_once_with(
            headers=self.test_headers,
            after=self.test_after,
            before=self.test_before,
            limit=self.test_limit
        )

    def test_fetch_news_handles_error(self):
        # Arrange
        test_error = Exception("Test error")
        self.mock_repository.invoke.side_effect = test_error

        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.use_case.fetch_news_connection(
                headers=self.test_headers,
                after=self.test_after,
                before=self.test_before,
                limit=self.test_limit
            )

        self.assertEqual(str(context.exception), "Test error")
        self.mock_repository.invoke.assert_called_once_with(
            headers=self.test_headers,
            after=self.test_after,
            before=self.test_before,
            limit=self.test_limit
        )
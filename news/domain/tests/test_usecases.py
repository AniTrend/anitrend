import unittest
from unittest.mock import Mock

import pytest

from news.data.repositories import NewsRepository
from news.data.schemas import NewsConnectionSchema, NewsSchema
from news.domain.usecases import NewsUseCase


class TestNewsUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repository = Mock(spec=NewsRepository)
        self.use_case = NewsUseCase(repository=self.mock_repository)
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
    def test_fetch_news_success(self):
        self.mock_repository.invoke.return_value = self.sample_news

        result = self.use_case.fetch_news_connection(
            headers=self.test_headers,
            after=self.test_after,
            before=self.test_before,
            limit=self.test_limit,
        )

        self.assertEqual(result, self.sample_news)
        self.mock_repository.invoke.assert_called_once_with(
            headers=self.test_headers,
            after=self.test_after,
            before=self.test_before,
            limit=self.test_limit,
        )

    @pytest.mark.integration
    def test_fetch_news_handles_error(self):
        test_error = Exception("Test error")
        self.mock_repository.invoke.side_effect = test_error

        with self.assertRaises(Exception) as context:
            self.use_case.fetch_news_connection(
                headers=self.test_headers,
                after=self.test_after,
                before=self.test_before,
                limit=self.test_limit,
            )

        self.assertEqual(str(context.exception), "Test error")
        self.mock_repository.invoke.assert_called_once_with(
            headers=self.test_headers,
            after=self.test_after,
            before=self.test_before,
            limit=self.test_limit,
        )

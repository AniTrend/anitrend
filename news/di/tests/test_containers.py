import unittest
from django.conf import settings

from news.di.containers import NewsContainer
from news.data.sources import RemoteSource
from news.data.repositories import NewsRepository
from news.domain.usecases import NewsUseCase


class TestNewsContainer(unittest.TestCase):
    def setUp(self):
        self.container = NewsContainer()
        self.container.init_resources()

    def test_remote_source_provider(self):
        remote_source = self.container.remote_source()
        self.assertIsInstance(remote_source, RemoteSource)

    def test_repository_provider(self):
        repository = self.container.repository()
        self.assertIsInstance(repository, NewsRepository)
        self.assertIsInstance(repository._remote_source, RemoteSource)

    def test_use_case_provider(self):
        use_case = self.container.use_case()
        self.assertIsInstance(use_case, NewsUseCase)
        self.assertIsInstance(use_case._repository, NewsRepository)
import unittest
from django.conf import settings
import pytest

from config.di.containers import ConfigContainer
from config.data.sources import RemoteSource
from config.data.repositories import Repository
from config.domain.usecases import ConfigUseCase


class TestConfigContainer(unittest.TestCase):
    def setUp(self):
        self.container = ConfigContainer()
        self.container.init_resources()

    @pytest.mark.integration
    def test_remote_source_provider(self):
        remote_source = self.container.remote_source()
        self.assertIsInstance(remote_source, RemoteSource)

    @pytest.mark.integration
    def test_repository_provider(self):
        repository = self.container.repository()
        self.assertIsInstance(repository, Repository)
        self.assertIsInstance(repository._remote_source, RemoteSource)

    @pytest.mark.integration
    def test_use_case_provider(self):
        use_case = self.container.use_case()
        self.assertIsInstance(use_case, ConfigUseCase)
        self.assertIsInstance(use_case._repository, Repository)

import unittest
import pytest

from media.di.containers import MediaContainer
from media.data.sources import RemoteSource
from media.data.repositories import Repository
from media.domain.usecases import MediaUseCase


class TestMediaContainer(unittest.TestCase):
    def setUp(self):
        self.container = MediaContainer()
        self.container.init_resources()

    def tearDown(self):
        self.container.shutdown_resources()

    @pytest.mark.integration  # You can add this if you categorize tests
    def test_remote_source_provider(self):
        remote_source = self.container.remote_source()
        self.assertIsInstance(
            remote_source, RemoteSource, "Expected RemoteSource instance from container"
        )

    @pytest.mark.integration
    def test_repository_provider(self):
        repository = self.container.repository()
        self.assertIsInstance(
            repository, Repository, "Expected Repository instance from container"
        )

    @pytest.mark.integration
    def test_use_case_provider(self):
        use_case = self.container.use_case()
        self.assertIsInstance(
            use_case, MediaUseCase, "Expected MediaUseCase instance from container"
        )

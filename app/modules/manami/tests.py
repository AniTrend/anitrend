from django.test import TestCase

from app.modules.common import FileSystem
from .di import UseCaseContainer, RepositoryContainer, RemoteSourceContainer
from .domain.entities import AnimeContainer
from .models import Anime


class DependenciesTestCase(TestCase):

    def test_remote_source_provider(self):
        remote_source = RemoteSourceContainer.remote_source()
        self.assertIsNotNone(remote_source)

    def test_repository_provider(self):
        repository = RepositoryContainer.repository()
        self.assertIsNotNone(repository)

    def test_use_case_provider(self):
        use_case = UseCaseContainer.use_case()
        self.assertIsNotNone(use_case)


class RepositoryTestCase(TestCase):

    def setUp(self):
        self.repository = RepositoryContainer.repository()
        data = FileSystem.get_file_contents(".samples", "manami_sample.json")
        self.container = AnimeContainer.from_json(data)
        self.assertIsNotNone(self.container)

    def test_repository_mappings_and_relation(self):
        self.repository.map_and_save_results(self.container)
        self.assertEqual(Anime.objects.count(), 6)

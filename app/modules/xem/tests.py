from django.test import TestCase

from app.modules.common import FileSystem
from .di import UseCaseContainer, RepositoryContainer, RemoteSourceContainer
from .domain.entities import XemContainer
from .models import Xem


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
        data = FileSystem.get_file_contents(".samples", "xem_sample.json")
        self.container = XemContainer.from_json(data)
        self.assertIsNotNone(self.container)

    def test_repository_mappings_and_relation(self):
        self.repository.map_and_save_results(self.container)
        self.assertEqual(Xem.objects.count(), 2)

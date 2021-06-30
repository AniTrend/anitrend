from django.test import TestCase

from app.modules.common import FileSystem
from .di import UseCaseContainer, RepositoryContainer, RemoteSourceContainer
from .domain.entities import CrunchyIndexContainer
from .models import CrunchyPanel


class DependenciesTestCase(TestCase):

    def test_cms_source_provider(self):
        remote_source = RemoteSourceContainer.cms_source()
        self.assertIsNotNone(remote_source)

    def test_token_source_provider(self):
        remote_source = RemoteSourceContainer.token_source()
        self.assertIsNotNone(remote_source)

    def test_signing_source_provider(self):
        remote_source = RemoteSourceContainer.signing_source()
        self.assertIsNotNone(remote_source)

    def test_bucket_repository_provider(self):
        repository = RepositoryContainer.bucket_repository()
        self.assertIsNotNone(repository)

    def test_signing_repository_provider(self):
        repository = RepositoryContainer.singing_repository()
        self.assertIsNotNone(repository)

    def test_cms_repository_provider(self):
        repository = RepositoryContainer.cms_repository()
        self.assertIsNotNone(repository)

    def test_use_case_provider(self):
        use_case = UseCaseContainer.use_case()
        self.assertIsNotNone(use_case)


class BucketRepositoryTestCase(TestCase):

    def setUp(self):
        self.repository = RepositoryContainer.bucket_repository()
        data = FileSystem.get_file_contents(".samples", "crunchy_sample.json")
        self.container = CrunchyIndexContainer.from_json(data)
        self.assertIsNotNone(self.container)

    def test_repository_mappings_and_relation(self):
        self.repository.map_and_save_results(self.container)
        self.assertEqual(CrunchyPanel.objects.count(), 26)

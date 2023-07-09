from django.test import TestCase

from core.helpers import FileSystem
from .data.schemas import IndexContainerSchema
from .di import UseCaseContainer, RepositoryContainer, RemoteSourceContainer


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
        repository = RepositoryContainer.signing_repository()
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
        data = FileSystem.get_file_contents(
            directory="fixtures/crunchy",
            file_name="index.json"
        )
        self.container = IndexContainerSchema().loads(data)

    def test_repository_deserialization(self):
        self.assertIsNotNone(self.container)

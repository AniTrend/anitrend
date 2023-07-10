from django.test import TestCase

from .di import UseCaseContainer, RepositoryContainer, RemoteSourceContainer


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

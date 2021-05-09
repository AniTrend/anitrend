from django.test import TestCase

from api.dependencies import RepositoryProvider


class DependenciesTestCase(TestCase):

    def test_repository_provider(self):
        session = RepositoryProvider.series_repository()
        self.assertIsNotNone(session)

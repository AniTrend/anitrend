from django.test import TestCase

from .di import SeriesRepositoryContainer


class DependenciesTestCase(TestCase):

    def test_repository_provider(self):
        session = SeriesRepositoryContainer.series_repository()
        self.assertIsNotNone(session)

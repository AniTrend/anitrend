from django.test import TestCase

from .di import MediaRepositoryContainer


class DependenciesTestCase(TestCase):

    def test_repository_provider(self):
        session = MediaRepositoryContainer.media_repository()
        self.assertIsNotNone(session)

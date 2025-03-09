from django.test import TestCase

from core.helpers import FileSystem
from config.di import RepositoryContainer
from config.data.schemas import ConfigurationSchema
from config.domain.entities import ConfigurationModel


class RepositoryTestCase(TestCase):

    def setUp(self):
        self.repository = RepositoryContainer.repository()
        data = FileSystem.get_file_contents("fixtures/edge", "config.json")
        self.model = ConfigurationSchema().loads(json_data=data)
        self.assertIsNotNone(self.model)

    def test_repository_mappings_and_relation(self):
        self.assertIsInstance(self.model, ConfigurationModel)

from django.test import TestCase

from core.helpers import FileSystem
from .di import UseCaseContainer, RepositoryContainer, RemoteSourceContainer
from .data.schemas import ConfigurationSchema
from .domain.entities import ConfigurationModel


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
        data = FileSystem.get_file_contents("fixtures/edge", "config.json")
        self.schema = ConfigurationSchema().loads(json_data=data)
        self.assertIsNotNone(self.schema)

    def test_repository_mappings_and_relation(self):
        # model = ConfigurationModel.from_dict(self.schema)
        # self.assertIsNotNone(model)
        pass

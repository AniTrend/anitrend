from django.test import TestCase

from service.dependencies import SessionProvider, RemoteSourceProvider, UseCaseProvider


class DependenciesTestCase(TestCase):

    def test_session_provider(self):
        session = SessionProvider.default_session()
        self.assertIsNotNone(session)

    def test_remote_source_xem_provider(self):
        xem_remote_source = RemoteSourceProvider.xem_remote_source()
        self.assertIsNotNone(xem_remote_source)

    def test_remote_source_relation_provider(self):
        relation_remote_source = RemoteSourceProvider.relation_remote_source()
        self.assertIsNotNone(relation_remote_source)

    def test_use_case_xem_provider(self):
        xem_use_case = UseCaseProvider.xem_use_case()
        self.assertIsNotNone(xem_use_case)

    def test_use_case_relation_provider(self):
        relation_use_case = UseCaseProvider.relation_use_case()
        self.assertIsNotNone(relation_use_case)
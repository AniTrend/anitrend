from django.test import TestCase


class DefaultTestCase(TestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_nothing(self):
        self.assertEqual(1, 1)

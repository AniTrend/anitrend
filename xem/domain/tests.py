import unittest

from core.helpers import FileSystem
from ..domain.entities import XemContainer


class EntityDeserializationTestCase(unittest.TestCase):

    def test_xem_deserialization(self):
        data = FileSystem.get_file_contents("fixtures/xem", "xem_sample.json")
        entity = XemContainer.from_json(data)
        self.assertIsNotNone(entity)


if __name__ == "__main__":
    unittest.main()

import unittest

from core.helpers import FileSystem
from ..domain.entities import AnimeContainer


class EntityDeserializationTestCase(unittest.TestCase):

    def test_manami_deserialization(self):
        data = FileSystem.get_file_contents("fixtures/manami", "manami_sample.json")
        entity = AnimeContainer.from_json(data)
        self.assertIsNotNone(entity)


if __name__ == "__main__":
    unittest.main()

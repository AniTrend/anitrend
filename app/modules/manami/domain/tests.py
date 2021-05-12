import unittest

from app.modules.common import FileSystem

from ..domain.entities import AnimeContainer


class EntityDeserializationTestCase(unittest.TestCase):

    def test_manami_deserialization(self):
        data = FileSystem.get_file_contents(".samples", "manami_sample.json")
        entity = AnimeContainer.from_json(data)
        self.assertIsNotNone(entity)


if __name__ == "__main__":
    unittest.main()

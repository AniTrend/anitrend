import unittest

from app.modules.common import FileSystem

from ..domain.entities import CrunchyIndexContainer


class EntityDeserializationTestCase(unittest.TestCase):
    def test_crunchy_deserialization(self):
        data = FileSystem.get_file_contents(".samples", "crunchy_sample.json")
        entity = CrunchyIndexContainer.from_json(data)
        self.assertIsNotNone(entity)


if __name__ == '__main__':
    unittest.main()

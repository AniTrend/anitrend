import unittest

from core.helpers import FileSystem
from ..domain.entities import CrunchyIndexContainer


class EntityDeserializationTestCase(unittest.TestCase):

    @unittest.skip('Pending rewrite')
    def test_crunchy_deserialization(self):
        data = FileSystem.get_file_contents(
            directory="fixtures/crunchy",
            file_name="index.json"
        )
        entity = CrunchyIndexContainer.from_json(data)
        self.assertIsNotNone(entity)


if __name__ == '__main__':
    unittest.main()

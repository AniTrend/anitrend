import unittest
from common import FileSystem
from model_entities import RelationContainerEntity, XemContainerEntity


class EntityDeserializationTestCase(unittest.TestCase):

    def test_xem_deserialization(self):
        data = FileSystem.get_file_contents("tests", "xem_sample.json")
        entity = XemContainerEntity.from_json(data)
        self.assertIsNotNone(entity)

    def test_relation_deserialization(self):
        data = FileSystem.get_file_contents("tests", "relation_sample.json")
        entity = RelationContainerEntity.from_json(data)
        self.assertIsNotNone(entity)


if __name__ == "__main__":
    unittest.main()

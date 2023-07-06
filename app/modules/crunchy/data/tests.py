import unittest

from core.helpers import FileSystem
from app.modules.crunchy.data.schemas import IndexSchema


class TestSchemaSuite(unittest.TestCase):

    @unittest.skip('Not implemented yet')
    def test_resource_schema(self):
        self.fail()

    @unittest.skip('Not implemented yet')
    def test_token_schema(self):
        self.fail()

    @unittest.skip('Not implemented yet')
    def test_signing_policy_schema(self):
        self.fail()

    @unittest.skip('Not implemented yet')
    def test_signing_policy_container_schema(self):
        self.fail()

    @unittest.skip('Not implemented yet')
    def test_series_panel_meta_schema(self):
        self.fail()

    @unittest.skip('Not implemented yet')
    def test_movie_panel_meta_schema(self):
        self.fail()

    @unittest.skip('Not implemented yet')
    def test_search_meta_schema(self):
        self.fail()

    @unittest.skip('Not implemented yet')
    def test_image_schema(self):
        self.fail()

    @unittest.skip('Not implemented yet')
    def test_image_container_schema(self):
        self.fail()

    @unittest.skip('Not implemented yet')
    def test_panel_schema(self):
        self.fail()

    def test_index_schema(self):
        data = FileSystem.get_file_contents(
            directory=".samples/crunchy",
            file_name="index.json"
        )
        schema = IndexSchema().from_json(content=data)
        self.assertIsInstance(schema.items, list)
        self.assertIsInstance(schema.num_items, int)
        self.assertIsInstance(schema.total_count, int)

    @unittest.skip('Not implemented yet')
    def test_index_container_schema(self):
        self.fail()

    @unittest.skip('Not implemented yet')
    def test_browse_container_schema(self):
        self.fail()

    @unittest.skip('Not implemented yet')
    def test_collection_container_schema(self):
        self.fail()

    @unittest.skip('Not implemented yet')
    def test_ad_break_schema(self):
        self.fail()

    @unittest.skip('Not implemented yet')
    def test_episode_schema(self):
        self.fail()

    @unittest.skip('Not implemented yet')
    def test_episode_container_schema(self):
        self.fail()

    @unittest.skip('Not implemented yet')
    def test_season_schema(self):
        self.fail()

    @unittest.skip('Not implemented yet')
    def test_season_container_schema(self):
        self.fail()

    @unittest.skip('Not implemented yet')
    def test_series_schema(self):
        self.fail()

    @unittest.skip('Not implemented yet')
    def test_movie_schema(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()

import json
import unittest
from unittest.mock import Mock

import pytest
from marshmallow_dataclass import class_schema

from core.helpers import FileSystem
from episode.data.repositories import EpisodeRepository
from episode.data.schemas import EpisodesResponse
from episode.data.sources import RemoteSource


class TestEpisodeRepository(unittest.TestCase):
    def setUp(self):
        self.mock_remote_source = Mock(spec=RemoteSource)
        self.repository = EpisodeRepository(remote_source=self.mock_remote_source)
        self.test_headers = {"Authorization": "Bearer test"}
        fixture_content = FileSystem.get_file_contents("fixtures/edge", "episodes.json")
        fixture_data = json.loads(fixture_content)
        schema = class_schema(EpisodesResponse)()
        self.sample_response = schema.load(fixture_data)

    @pytest.mark.integration
    def test_invoke_success(self):
        self.mock_remote_source.get_episodes.return_value = self.sample_response

        result = self.repository.invoke(
            mal_id=1,
            headers=self.test_headers,
            limit=10,
            after="after_cursor",
            before="before_cursor",
            kind="main",
            specials_only=False,
            start=1,
            end=12,
            include_orphans=False,
        )

        self.assertEqual(result, self.sample_response)
        self.mock_remote_source.get_episodes.assert_called_once_with(
            headers=self.test_headers,
            mal_id=1,
            limit=10,
            after="after_cursor",
            before="before_cursor",
            kind="main",
            specials_only=False,
            start=1,
            end=12,
            include_orphans=False,
        )

    @pytest.mark.integration
    def test_invoke_requires_mal_id(self):
        with self.assertRaises(ValueError):
            self.repository.invoke(headers=self.test_headers)

        self.mock_remote_source.get_episodes.assert_not_called()

    @pytest.mark.integration
    def test_invoke_propagates_error(self):
        self.mock_remote_source.get_episodes.side_effect = Exception("failure")

        with self.assertRaises(Exception):
            self.repository.invoke(mal_id=1, headers=self.test_headers)

        self.mock_remote_source.get_episodes.assert_called_once_with(
            headers=self.test_headers,
            mal_id=1,
            limit=None,
            after=None,
            before=None,
            kind=None,
            specials_only=None,
            start=None,
            end=None,
            include_orphans=None,
        )

import json
import unittest
from unittest.mock import Mock

import pytest
from marshmallow_dataclass import class_schema

from core.helpers import FileSystem
from episode.data.repositories import EpisodeRepository
from episode.data.schemas import EpisodesResponse
from episode.domain.usecases import EpisodeUseCase


class TestEpisodeUseCase(unittest.TestCase):
    def setUp(self):
        fixture_content = FileSystem.get_file_contents("fixtures/edge", "episodes.json")
        fixture_data = json.loads(fixture_content)
        schema = class_schema(EpisodesResponse)()
        self.sample_response = schema.load(fixture_data)

        self.mock_repository = Mock(spec=EpisodeRepository)
        self.use_case = EpisodeUseCase(repository=self.mock_repository)
        self.test_headers = {"Authorization": "Bearer test"}

    @pytest.mark.unit
    def test_fetch_episodes_success(self):
        self.mock_repository.invoke.return_value = self.sample_response

        result = self.use_case.fetch_episodes(
            mal_id=1,
            headers=self.test_headers,
            limit=5,
            after="after_cursor",
            before="before_cursor",
            kind="main",
            specials_only=True,
            start=1,
            end=10,
            include_orphans=True,
        )

        self.assertEqual(result, self.sample_response)
        self.mock_repository.invoke.assert_called_once_with(
            mal_id=1,
            headers=self.test_headers,
            limit=5,
            after="after_cursor",
            before="before_cursor",
            kind="main",
            specials_only=True,
            start=1,
            end=10,
            include_orphans=True,
        )

    @pytest.mark.unit
    def test_fetch_episodes_handles_error(self):
        test_error = Exception("fetch failure")
        self.mock_repository.invoke.side_effect = test_error

        with self.assertRaises(Exception) as context:
            self.use_case.fetch_episodes(mal_id=1, headers=self.test_headers)

        self.assertEqual(str(context.exception), "fetch failure")
        self.mock_repository.invoke.assert_called_once_with(
            mal_id=1,
            headers=self.test_headers,
            limit=None,
            after=None,
            before=None,
            kind=None,
            specials_only=None,
            start=None,
            end=None,
            include_orphans=None,
        )

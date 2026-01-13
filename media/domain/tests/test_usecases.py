import unittest
from unittest.mock import Mock, patch
import json
from typing import cast

import pytest
from marshmallow_dataclass import class_schema

from media.data.repositories import Repository
from media.data.schemas import MediaEntity
from media.domain.usecases import MediaUseCase
from core.helpers import FileSystem


class TestMediaUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repository = Mock(spec=Repository)
        self.use_case = MediaUseCase(repository=self.mock_repository)
        self.test_headers = {"Authorization": "Bearer test"}
        self.test_series_id = 150075

        fixture_content = FileSystem.get_file_contents("fixtures/edge", "media.json")
        raw_fixture_data = json.loads(fixture_content)

        try:
            MediaEntitySchema = class_schema(MediaEntity)()
            self.sample_media = cast(
                MediaEntity, MediaEntitySchema.load(raw_fixture_data)
            )
        except Exception as e:
            self.fail(f"Failed to load Media from fixture data in setUp: {e}")

    @pytest.mark.unit
    def test_fetch_series_by_id_success(self):
        self.mock_repository.invoke.return_value = self.sample_media

        result = self.use_case.fetch_series_by_id(
            series_id=self.test_series_id, headers=self.test_headers
        )

        self.assertEqual(result, self.sample_media)
        self.mock_repository.invoke.assert_called_once_with(
            anilist=self.test_series_id, headers=self.test_headers
        )

    @pytest.mark.unit
    @patch("media.domain.usecases.MediaUseCase._logger")
    def test_fetch_series_by_id_handles_repository_error(self, mock_logger):
        test_error = Exception("Repository error")
        self.mock_repository.invoke.side_effect = test_error

        with self.assertRaises(Exception) as context:
            self.use_case.fetch_series_by_id(
                series_id=self.test_series_id, headers=self.test_headers
            )

        self.assertEqual(str(context.exception), "Repository error")
        self.mock_repository.invoke.assert_called_once_with(
            anilist=self.test_series_id, headers=self.test_headers
        )
        mock_logger.error.assert_called_once_with(
            f"Uncaught exception while fetching series_id {self.test_series_id}",
            exc_info=test_error,
        )

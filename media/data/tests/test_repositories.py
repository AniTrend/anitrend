from typing import cast
import unittest
from unittest.mock import Mock, patch
from json import JSONDecodeError
import json

from marshmallow_dataclass import class_schema
import pytest

from media.data.repositories import Repository
from media.data.schemas import MediaApiResponse, MediaEntity
from media.data.sources import RemoteSource
from core.helpers import FileSystem


class TestMediaRepository(unittest.TestCase):
    def setUp(self):
        self.mock_remote_source = Mock(spec=RemoteSource)
        self.repository = Repository(remote_source=self.mock_remote_source)
        self.test_headers = {"Authorization": "Bearer test"}
        self.test_series_id = 150075

        fixture_content = FileSystem.get_file_contents("fixtures/edge", "media.json")
        self.raw_fixture_data = json.loads(fixture_content)

        media_data_from_fixture = self.raw_fixture_data.get("data", {})
        try:
            MediaEntitySchema = class_schema(MediaEntity)()
            self.sample_media = cast(
                MediaEntity, MediaEntitySchema.load(media_data_from_fixture)
            )
        except Exception as e:
            self.fail(f"Failed to load Media from prepared fixture data: {e}")
        self.sample_api_response = MediaApiResponse(data=self.sample_media)

    @pytest.mark.integration
    def test_invoke_success(self):
        self.mock_remote_source.get_series_by_id.return_value = self.sample_api_response

        result = self.repository.invoke(
            series_id=self.test_series_id, headers=self.test_headers
        )

        self.assertEqual(result, self.sample_media)
        self.mock_remote_source.get_series_by_id.assert_called_once_with(
            series_id=self.test_series_id, headers=self.test_headers
        )

    @pytest.mark.integration
    def test_invoke_handles_json_decode_error(self):
        json_error = JSONDecodeError("Invalid JSON", "test", 0)
        self.mock_remote_source.get_series_by_id.side_effect = json_error

        with self.assertRaises(JSONDecodeError):
            self.repository.invoke(
                series_id=self.test_series_id, headers=self.test_headers
            )

        self.mock_remote_source.get_series_by_id.assert_called_once_with(
            series_id=self.test_series_id, headers=self.test_headers
        )

    @pytest.mark.integration
    def test_invoke_handles_value_error_when_no_data(self):
        empty_response = MediaApiResponse(data=None)
        self.mock_remote_source.get_series_by_id.return_value = empty_response

        with self.assertRaisesRegex(
            ValueError, f"No data found for series_id {self.test_series_id}"
        ):
            self.repository.invoke(
                series_id=self.test_series_id, headers=self.test_headers
            )
        self.mock_remote_source.get_series_by_id.assert_called_once_with(
            series_id=self.test_series_id, headers=self.test_headers
        )

    @pytest.mark.integration
    def test_invoke_handles_type_error_when_data_is_wrong_type(self):
        wrong_type_response = MediaApiResponse(data="not a Media object")  # type: ignore
        self.mock_remote_source.get_series_by_id.return_value = wrong_type_response

        expected_error_message = f"Expected MediaEntity type but got {type(str())} for series_id {self.test_series_id}"

        with self.assertRaisesRegex(TypeError, expected_error_message):
            self.repository.invoke(
                series_id=self.test_series_id, headers=self.test_headers
            )
        self.mock_remote_source.get_series_by_id.assert_called_once_with(
            series_id=self.test_series_id, headers=self.test_headers
        )

    @pytest.mark.integration
    @patch("media.data.repositories.Repository._logger")
    def test_invoke_general_exception(self, mock_logger):
        generic_exception = Exception("Something went wrong")
        self.mock_remote_source.get_series_by_id.side_effect = generic_exception

        with self.assertRaisesRegex(Exception, "Something went wrong"):
            self.repository.invoke(
                series_id=self.test_series_id, headers=self.test_headers
            )

        self.mock_remote_source.get_series_by_id.assert_called_once_with(
            series_id=self.test_series_id, headers=self.test_headers
        )

        mock_logger.error.assert_any_call(
            f"An unexpected error occurred while fetching series_id {self.test_series_id}",
            exc_info=generic_exception,
        )

from typing import cast
import unittest
from unittest.mock import Mock, patch
from json import JSONDecodeError
import json

from marshmallow_dataclass import class_schema
import pytest

from media.data.repositories import Repository
from media.data.schemas import MediaEntity
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
        try:
            MediaEntitySchema = class_schema(MediaEntity)()
            self.sample_media = cast(
                MediaEntity, MediaEntitySchema.load(self.raw_fixture_data)
            )
        except Exception as e:
            self.fail(f"Failed to load Media from prepared fixture data: {e}")

    @pytest.mark.integration
    def test_invoke_success(self):
        self.mock_remote_source.get_series.return_value = self.sample_media

        result = self.repository.invoke(
            anilist=self.test_series_id, headers=self.test_headers
        )

        self.assertEqual(result, self.sample_media)
        self.mock_remote_source.get_series.assert_called_once_with(
            headers=self.test_headers,
            anilist=self.test_series_id,
            trakt=None,
            tvdb=None,
            tmdb=None,
            mal=None,
            notify=None,
            slug=None,
        )

    @pytest.mark.integration
    def test_invoke_supports_multiple_identifiers(self):
        self.mock_remote_source.get_series.return_value = self.sample_media

        result = self.repository.invoke(
            anilist=self.test_series_id,
            trakt=123,
            tvdb=456,
            tmdb=789,
            mal=321,
            notify="notifier",
            slug="media-slug",
            headers=self.test_headers,
        )

        self.assertEqual(result, self.sample_media)
        self.mock_remote_source.get_series.assert_called_once_with(
            headers=self.test_headers,
            anilist=self.test_series_id,
            trakt=123,
            tvdb=456,
            tmdb=789,
            mal=321,
            notify="notifier",
            slug="media-slug",
        )

    @pytest.mark.integration
    def test_invoke_handles_json_decode_error(self):
        json_error = JSONDecodeError("Invalid JSON", "test", 0)
        self.mock_remote_source.get_series.side_effect = json_error

        with self.assertRaises(JSONDecodeError):
            self.repository.invoke(
                anilist=self.test_series_id, headers=self.test_headers
            )

        self.mock_remote_source.get_series.assert_called_once_with(
            headers=self.test_headers,
            anilist=self.test_series_id,
            trakt=None,
            tvdb=None,
            tmdb=None,
            mal=None,
            notify=None,
            slug=None,
        )

    @pytest.mark.integration
    def test_invoke_handles_value_error_when_no_data(self):
        self.mock_remote_source.get_series.return_value = None

        with self.assertRaisesRegex(
            ValueError, "No data found for provided identifiers"
        ):
            self.repository.invoke(
                anilist=self.test_series_id, headers=self.test_headers
            )
        self.mock_remote_source.get_series.assert_called_once_with(
            headers=self.test_headers,
            anilist=self.test_series_id,
            trakt=None,
            tvdb=None,
            tmdb=None,
            mal=None,
            notify=None,
            slug=None,
        )

    @pytest.mark.integration
    def test_invoke_handles_type_error_when_data_is_wrong_type(self):
        wrong_type_response = "not a Media object"  # type: ignore
        self.mock_remote_source.get_series.return_value = wrong_type_response

        expected_error_message = (
            f"Expected MediaEntity type but got {type(str())} for provided identifiers"
        )

        with self.assertRaisesRegex(TypeError, expected_error_message):
            self.repository.invoke(
                anilist=self.test_series_id, headers=self.test_headers
            )
        self.mock_remote_source.get_series.assert_called_once_with(
            headers=self.test_headers,
            anilist=self.test_series_id,
            trakt=None,
            tvdb=None,
            tmdb=None,
            mal=None,
            notify=None,
            slug=None,
        )

    @pytest.mark.integration
    @patch("media.data.repositories.Repository._logger")
    def test_invoke_general_exception(self, mock_logger):
        generic_exception = Exception("Something went wrong")
        self.mock_remote_source.get_series.side_effect = generic_exception

        with self.assertRaisesRegex(Exception, "Something went wrong"):
            self.repository.invoke(
                anilist=self.test_series_id, headers=self.test_headers
            )

        self.mock_remote_source.get_series.assert_called_once_with(
            headers=self.test_headers,
            anilist=self.test_series_id,
            trakt=None,
            tvdb=None,
            tmdb=None,
            mal=None,
            notify=None,
            slug=None,
        )

        mock_logger.error.assert_any_call(
            f"An unexpected error occurred while fetching identifiers {{'anilist': {self.test_series_id}, 'trakt': None, 'tvdb': None, 'tmdb': None, 'mal': None, 'notify': None, 'slug': None}}",
            exc_info=generic_exception,
        )

    def test_invoke_requires_at_least_one_identifier(self):
        with self.assertRaisesRegex(
            ValueError,
            "At least one identifier (anilist/trakt/tvdb/tmdb/mal/notify/slug) is required",
        ):
            self.repository.invoke(headers=self.test_headers)

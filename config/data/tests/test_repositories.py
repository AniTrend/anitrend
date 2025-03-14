import unittest
from unittest.mock import Mock
from json import JSONDecodeError

import pytest

from config.data.repositories import Repository
from config.data.schemas import ConfigurationSchema, SettingsSchema
from config.data.sources import RemoteSource


class TestConfigRepository(unittest.TestCase):
    def setUp(self):
        self.mock_remote_source = Mock(spec=RemoteSource)
        self.repository = Repository(remote_source=self.mock_remote_source)
        self.test_headers = {"Authorization": "Bearer test"}

        self.sample_config = ConfigurationSchema(
            id="test",
            settings=SettingsSchema(analyticsEnabled=True, platformSource="test"),
            image=None,
            navigation=None,
            genres=None,
        )

    @pytest.mark.integration
    def test_invoke_success(self):
        self.mock_remote_source.get_config.return_value = self.sample_config

        result = self.repository.invoke(headers=self.test_headers)

        self.assertEqual(result, self.sample_config)
        self.mock_remote_source.get_config.assert_called_once_with(
            headers=self.test_headers
        )

    @pytest.mark.integration
    def test_invoke_handles_json_decode_error(self):
        json_error = JSONDecodeError("Invalid JSON", "test", 0)
        self.mock_remote_source.get_config.side_effect = json_error

        with self.assertRaises(JSONDecodeError):
            self.repository.invoke(headers=self.test_headers)

        self.mock_remote_source.get_config.assert_called_once_with(
            headers=self.test_headers
        )

import unittest
from unittest.mock import Mock
from json import JSONDecodeError

import pytest

from config.data.repositories import Repository
from config.data.schemas import (
    ConfigurationSchema,
    GenreSchema,
    ImageSchema,
    NavigationGroupSchema,
    NavigationSchema,
    SettingsSchema,
)
from config.data.sources import RemoteSource


class TestConfigRepository(unittest.TestCase):
    def setUp(self):
        self.mock_remote_source = Mock(spec=RemoteSource)
        self.repository = Repository(remote_source=self.mock_remote_source)
        self.test_headers = {"Authorization": "Bearer test"}

        self.sample_config = ConfigurationSchema(
            id="c5f575b4-4f7e-4fbe-8c87-4b7cfb3c7d1c",
            settings=SettingsSchema(analyticsEnabled=True, platformSource="https://example.com"),
            image=ImageSchema(
                banner="https://example.com/banner.jpg",
                poster="https://example.com/poster.jpg",
                loading="https://example.com/loading.jpg",
                error="https://example.com/error.jpg",
                info="https://example.com/info.jpg",
                default="https://example.com/default.jpg",
            ),
            navigation=[
                NavigationSchema(
                    criteria="home",
                    destination="/home",
                    i18n="home.label",
                    icon="home",
                    group=NavigationGroupSchema(authenticated=False, i18n="group.public"),
                )
            ],
            genres=[GenreSchema(name="Action", mediaId=1)],
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

import unittest
from unittest.mock import Mock

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
from config.domain.usecases import ConfigUseCase


class TestConfigUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repository = Mock(spec=Repository)
        self.use_case = ConfigUseCase(repository=self.mock_repository)
        self.test_headers = {"Authorization": "Bearer test"}

        self.sample_config = ConfigurationSchema(
            id="test",
            settings=SettingsSchema(analyticsEnabled=True, platformSource="test"),
            image=ImageSchema(
                banner="banner.jpg",
                poster="poster.jpg",
                loading="loading.svg",
                error="error.svg",
                info="info.svg",
                default="default.svg",
            ),
            navigation=[
                NavigationSchema(
                    criteria=">=2.0.0",
                    destination="/home",
                    i18n="navigation_home",
                    icon="ic_home_24",
                    group=NavigationGroupSchema(
                        authenticated=False, i18n="navigation_header_general"
                    ),
                )
            ],
            genres=[GenreSchema(name="Action", mediaId=101922)],
        )

    @pytest.mark.integration
    def test_fetch_config_success(self):
        self.mock_repository.invoke.return_value = self.sample_config

        result = self.use_case.fetch_configuration(headers=self.test_headers)

        self.assertEqual(result, self.sample_config)
        self.mock_repository.invoke.assert_called_once_with(headers=self.test_headers)

    @pytest.mark.integration
    def test_fetch_config_handles_error(self):
        test_error = Exception("Test error")
        self.mock_repository.invoke.side_effect = test_error

        with self.assertRaises(Exception) as context:
            self.use_case.fetch_configuration(headers=self.test_headers)

        self.assertEqual(str(context.exception), "Test error")
        self.mock_repository.invoke.assert_called_once_with(headers=self.test_headers)

import unittest
from unittest.mock import Mock

from config.domain.entities import ConfigurationModel, SettingsModel
from config.domain.usecases import ConfigUseCase
from core.repositories import DataRepository


class TestConfigUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repository = Mock(spec=DataRepository)
        self.config_use_case = ConfigUseCase(repository=self.mock_repository)
        self.sample_config = ConfigurationModel(
            settings=SettingsModel(
                analyticsEnabled=True,
                platformSource="test"
            ),
            image=None,
            navigation=None,
            genres=None
        )

    def test_fetch_configuration_success(self):
        # Arrange
        test_headers = {"Authorization": "Bearer test"}
        self.mock_repository.invoke.return_value = self.sample_config

        # Act
        result = self.config_use_case.fetch_configuration(test_headers)

        # Assert
        self.assertEqual(result, self.sample_config)
        self.mock_repository.invoke.assert_called_once_with(headers=test_headers)

    def test_fetch_configuration_returns_none(self):
        # Arrange
        test_headers = {"Authorization": "Bearer test"}
        self.mock_repository.invoke.return_value = None

        # Act
        result = self.config_use_case.fetch_configuration(test_headers)

        # Assert
        self.assertIsNone(result)
        self.mock_repository.invoke.assert_called_once_with(headers=test_headers)

    def test_fetch_configuration_handles_exception(self):
        # Arrange
        test_headers = {"Authorization": "Bearer test"}
        self.mock_repository.invoke.side_effect = Exception("Test error")

        # Act & Assert
        with self.assertRaises(Exception) as exc_info:
            self.config_use_case.fetch_configuration(test_headers)

        self.assertEqual(str(exc_info.exception), "Test error")
        self.mock_repository.invoke.assert_called_once_with(headers=test_headers)

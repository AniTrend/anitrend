from typing import Any, Optional

from .entities import ConfigurationModel
from core.usecases import CommonUseCase


class ConfigUseCase(CommonUseCase):

    def fetch_configuration(self) -> Optional[ConfigurationModel]:
        try:
            data = self._repository.invoke()
            return data
        except Exception as e:
            self._logger.error(f"Uncaught exception", exc_info=e)
            raise e

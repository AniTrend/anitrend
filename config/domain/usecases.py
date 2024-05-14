from typing import Optional, Mapping

from .entities import ConfigurationModel
from core.usecases import CommonUseCase


class ConfigUseCase(CommonUseCase):

    def fetch_configuration(self, headers: Mapping) -> Optional[ConfigurationModel]:
        try:
            data = self._repository.invoke(headers=headers)
            return data
        except Exception as e:
            self._logger.error(f"Uncaught exception", exc_info=e)
            raise e

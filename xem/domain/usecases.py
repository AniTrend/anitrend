from typing import Optional, Any

from core.usecases import CommonUseCase


class XemUseCase(CommonUseCase):

    def fetch_all_mappings(self) -> Optional[Any]:
        try:
            data = self._repository.invoke()
            return data
        except Exception as e:
            self._logger.error(f"Uncaught exception", exc_info=e)
            raise e

from typing import Optional, Any

from app.modules.common.usecases import CommonUseCase


class CrunchyUseCase(CommonUseCase):

    def fetch_all_series(self) -> Optional[Any]:
        try:
            data = self._repository.invoke()
            return data
        except Exception as e:
            self._logger.error(f"Uncaught exception", exc_info=e)
            raise e

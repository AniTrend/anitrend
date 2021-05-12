from typing import Any, Optional

from app.modules.common.usecases import CommonUseCase


class ManAniUseCase(CommonUseCase):

    def fetch_all_records(self) -> Optional[Any]:
        try:
            data = self._repository.invoke()
            return data
        except Exception as e:
            self._logger.error(f"Uncaught exception", exc_info=e)
            raise e

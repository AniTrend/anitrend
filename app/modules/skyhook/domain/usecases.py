from typing import Any, Optional

from app.modules.common.usecases import CommonUseCase


class SkyhookUseCase(CommonUseCase):

    def find_series_by_tvdb_id(self, tvdb_id: int) -> Optional[Any]:
        try:
            data = self._repository.invoke(tvdb_id=tvdb_id)
            return data
        except Exception as e:
            self._logger.error(f"Uncaught exception", exc_info=e)
            raise e

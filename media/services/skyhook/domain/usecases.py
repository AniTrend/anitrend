from typing import Optional

from core.usecases import CommonUseCase
from ..domain.entities import SkyhookShow


class SkyhookUseCase(CommonUseCase):

    def find_series_by_tvdb_id(self, tvdb_id: int) -> Optional[SkyhookShow]:
        try:
            data = self._repository.invoke(tvdb_id=tvdb_id)
            return data
        except Exception as e:
            self._logger.error(f"Uncaught exception", exc_info=e)
            raise e

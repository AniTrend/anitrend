from typing import Optional, Mapping

from media.data.schemas import MediaEntity
from core.usecases import CommonUseCase


class MediaUseCase(CommonUseCase):

    def fetch_series_by_id(
        self, series_id: int, headers: Optional[Mapping[str, str]]
    ) -> Optional[MediaEntity]:
        try:
            data = self._repository.invoke(anilist=series_id, headers=headers)
            return data
        except Exception as e:
            self._logger.error(
                f"Uncaught exception while fetching series_id {series_id}", exc_info=e
            )
            raise e

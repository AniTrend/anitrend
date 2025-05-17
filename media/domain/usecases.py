from typing import Optional, Mapping

from ..data.schemas import Media
from ..data.repositories import (
    Repository,
)  # Ensure this points to media.data.repositories
from core.usecases import CommonUseCase


class MediaUseCase(CommonUseCase):
    _repository: Repository  # Specifically type hint for Media Repository

    def __init__(self, repository: Repository, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._repository = repository

    def fetch_series_by_id(self, series_id: int, headers: Mapping) -> Optional[Media]:
        try:
            # Headers will be passed via kwargs in the repository call if needed by RemoteSource
            data = self._repository.get_series_by_id(
                series_id=series_id, headers=headers
            )
            return data
        except Exception as e:
            # Log the specific series_id for better debugging
            self._logger.error(
                f"Uncaught exception while fetching series_id {series_id}", exc_info=e
            )
            raise e

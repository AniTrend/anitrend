from typing import Optional, Mapping

from media.data.schemas import MediaEntity
from core.usecases import CommonUseCase


class MediaUseCase(CommonUseCase):

    def fetch_series(
        self,
        headers: Optional[Mapping[str, str]],
        anilist: Optional[int] = None,
        mal: Optional[int] = None,
        trakt: Optional[int] = None,
        slug: Optional[str] = None,
        tvdb: Optional[int] = None,
        tmdb: Optional[int] = None,
        notify: Optional[str] = None,
    ) -> Optional[MediaEntity]:
        try:
            data = self._repository.invoke(
                headers=headers,
                anilist=anilist,
                mal=mal,
                trakt=trakt,
                slug=slug,
                tvdb=tvdb,
                tmdb=tmdb,
                notify=notify,
            )
            return data
        except Exception as e:
            self._logger.error("Uncaught exception while fetching series", exc_info=e)
            raise e

    def fetch_series_by_id(
        self,
        series_id: int,
        headers: Optional[Mapping[str, str]],
    ) -> Optional[MediaEntity]:
        try:
            return self._repository.invoke(series_id=series_id, headers=headers)
        except Exception as e:
            self._logger.error(
                f"Uncaught exception while fetching series_id {series_id}",
                exc_info=e,
            )
            raise e

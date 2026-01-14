from typing import Optional, Mapping

from media.data.schemas import MediaEntity
from core.usecases import CommonUseCase


class MediaUseCase(CommonUseCase):

    def fetch_series(
        self,
        headers: Optional[Mapping[str, str]],
        anilist: Optional[int] = None,
        trakt: Optional[int] = None,
        tvdb: Optional[int] = None,
        tmdb: Optional[int] = None,
        mal: Optional[int] = None,
        notify: Optional[str] = None,
        slug: Optional[str] = None,
    ) -> Optional[MediaEntity]:
        try:
            data = self._repository.invoke(
                headers=headers,
                anilist=anilist,
                trakt=trakt,
                tvdb=tvdb,
                tmdb=tmdb,
                mal=mal,
                notify=notify,
                slug=slug,
            )
            return data
        except Exception as e:
            self._logger.error(
                "Uncaught exception while fetching media via identifiers",
                exc_info=e,
            )
            raise e

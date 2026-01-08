from typing import Dict, Optional

from core.usecases import CommonUseCase
from episode.data.schemas import EpisodesResponse


class EpisodeUseCase(CommonUseCase):
    def fetch_episodes(
        self,
        mal_id: int,
        headers: Dict[str, str],
        limit: Optional[int] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        kind: Optional[str] = None,
        specials_only: Optional[bool] = None,
        start: Optional[int] = None,
        end: Optional[int] = None,
        include_orphans: Optional[bool] = None,
    ) -> EpisodesResponse:
        try:
            return self._repository.invoke(  # type: ignore[attr-defined]
                mal_id=mal_id,
                headers=headers,
                limit=limit,
                after=after,
                before=before,
                kind=kind,
                specials_only=specials_only,
                start=start,
                end=end,
                include_orphans=include_orphans,
            )
        except Exception as exc:  # pragma: no cover - logged and re-raised
            self._logger.error(
                f"Failed to fetch episodes for mal_id {mal_id}", exc_info=exc
            )
            raise

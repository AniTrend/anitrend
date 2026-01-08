from typing import Any, cast

from uplink import HeaderMap

from core.repositories import DataRepository
from episode.data.schemas import EpisodesResponse
from episode.data.sources import RemoteSource


class EpisodeRepository(DataRepository):
    _remote_source: RemoteSource

    def invoke(self, **kwargs: Any) -> EpisodesResponse:
        headers_value = kwargs.get("headers") or {}
        headers = cast(HeaderMap, headers_value)
        mal_id = kwargs.get("mal_id")
        if mal_id is None:
            raise ValueError("mal_id is required")

        try:
            response = self._remote_source.get_episodes(  # type: ignore[arg-type]
                headers=headers,
                mal_id=int(mal_id),
                limit=kwargs.get("limit"),
                after=kwargs.get("after"),
                before=kwargs.get("before"),
                kind=kwargs.get("kind"),
                specials_only=kwargs.get("specials_only"),
                start=kwargs.get("start"),
                end=kwargs.get("end"),
                include_orphans=kwargs.get("include_orphans"),
            )
            return response
        except Exception as exc:  # pragma: no cover - logged and re-raised
            self._logger.error("Failed to fetch episodes", exc_info=exc)
            raise

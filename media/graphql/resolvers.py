from typing import Optional

from strawberry.types.info import ContextType

from core.utilities import get_forwarded_headers

from media.di.containers import MediaContainer
from .types import MediaType


def resolve_media(
    context: ContextType,
    anilist: Optional[int] = None,
    trakt: Optional[int] = None,
    tvdb: Optional[int] = None,
    tmdb: Optional[int] = None,
    mal: Optional[int] = None,
    notify: Optional[str] = None,
    slug: Optional[str] = None,
    use_case_provider=MediaContainer.use_case,
) -> Optional[MediaType]:
    use_case = use_case_provider()
    forwarded_headers = get_forwarded_headers(context)  # type: ignore[arg-type]
    media_entity = use_case.fetch_series(
        headers=forwarded_headers,
        anilist=anilist,
        trakt=trakt,
        tvdb=tvdb,
        tmdb=tmdb,
        mal=mal,
        notify=notify,
        slug=slug,
    )
    if media_entity is None:
        return None
    return MediaType.from_entity(media_entity)

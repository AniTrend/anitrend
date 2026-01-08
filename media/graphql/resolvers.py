from typing import Optional

from strawberry.types.info import ContextType

from core.utilities import get_forwarded_headers

from media.di.containers import MediaContainer
from .types import MediaType


def resolve_media(
    context: ContextType,
    anilist: Optional[int] = None,
    mal: Optional[int] = None,
    trakt: Optional[int] = None,
    slug: Optional[str] = None,
    tvdb: Optional[int] = None,
    tmdb: Optional[int] = None,
    notify: Optional[str] = None,
    use_case_provider=MediaContainer.use_case,
) -> Optional[MediaType]:
    forwarded_headers = get_forwarded_headers(context)  # type: ignore[arg-type]
    media_entity = use_case_provider().fetch_series(
        headers=forwarded_headers,
        anilist=anilist,
        mal=mal,
        trakt=trakt,
        slug=slug,
        tvdb=tvdb,
        tmdb=tmdb,
        notify=notify,
    )
    if media_entity is None:
        return None
    return MediaType.from_entity(media_entity)

from typing import Optional

from strawberry.types.info import ContextType

from core.utilities import get_forwarded_headers

from media.di.containers import MediaContainer
from .types import MediaType


def resolve_media_by_id(
    context: ContextType, series_id: int, use_case_provider=MediaContainer.use_case
) -> Optional[MediaType]:
    use_case = use_case_provider()
    forwarded_headers = get_forwarded_headers(context)  # type: ignore[arg-type]
    media_entity = use_case.fetch_series_by_id(
        series_id=series_id, headers=forwarded_headers
    )
    if media_entity is None:
        return None
    return MediaType.from_entity(media_entity)

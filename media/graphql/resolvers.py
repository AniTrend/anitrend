from typing import Optional
import strawberry
from strawberry.types import Info

from ..di.containers import MediaContainer
from .types import MediaType

# Placeholder for media GraphQL resolvers


def resolve_media_by_id(info: Info, id: int) -> Optional[MediaType]:
    """Resolver function to fetch a media entity by its unique ID."""
    # Ensure MediaContainer is available in context
    media_container: MediaContainer = info.context.media_container  # type: ignore
    use_case = media_container.use_case()

    # Extract headers if your use case or repository needs them
    headers = info.context.request.headers

    media_entity = use_case.fetch_series_by_id(series_id=id, headers=headers)

    if media_entity:
        # Strawberry handles the mapping from dataclass to Strawberry type
        return media_entity  # type: ignore
    return None

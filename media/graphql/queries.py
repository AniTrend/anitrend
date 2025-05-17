import strawberry
from typing import Optional
from strawberry.types import Info

from .types import MediaType
from .resolvers import resolve_media_by_id


@strawberry.type
class MediaQuery:

    @strawberry.field(description="Fetch a media entity by its unique ID")
    def media_by_id(self, info: Info, id: int) -> Optional[MediaType]:
        return resolve_media_by_id(context=info.context, series_id=id)

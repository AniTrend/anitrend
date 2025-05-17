import strawberry
from typing import Optional
from strawberry.types import Info

from .types import MediaType
from .resolvers import resolve_media_by_id  # Import the resolver


@strawberry.type
class MediaQuery:
    @strawberry.field
    def media_by_id(self, info: Info, id: int) -> Optional[MediaType]:
        """Fetches a media entity by its unique ID."""
        # Delegate to the resolver function
        return resolve_media_by_id(info=info, id=id)

    # The hello_media field can be removed if no longer needed, or kept for testing.
    # @strawberry.field
    # def hello_media(self) -> str:
    #     return "Hi from media!"

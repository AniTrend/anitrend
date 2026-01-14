import strawberry
from typing import Optional
from strawberry.types import Info

from .types import MediaType
from .resolvers import resolve_media


@strawberry.type
class MediaQuery:

    @strawberry.field(
        description="Fetch a media entity by upstream identifiers (at least one required)"
    )
    def media(
        self,
        info: Info,
        anilist: Optional[int] = None,
        trakt: Optional[int] = None,
        tvdb: Optional[int] = None,
        tmdb: Optional[int] = None,
        mal: Optional[int] = None,
        notify: Optional[str] = None,
        slug: Optional[str] = None,
    ) -> Optional[MediaType]:
        return resolve_media(
            context=info.context,
            anilist=anilist,
            trakt=trakt,
            tvdb=tvdb,
            tmdb=tmdb,
            mal=mal,
            notify=notify,
            slug=slug,
        )

    @strawberry.field(
        description="Fetch a media entity by its AniList ID",
        deprecation_reason="Use media(anilist: Int) instead",
    )
    def media_by_anilist(self, info: Info, anilist_id: int) -> Optional[MediaType]:
        return resolve_media(
            context=info.context,
            anilist=anilist_id,
        )

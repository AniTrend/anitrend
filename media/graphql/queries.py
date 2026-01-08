import strawberry
from typing import Optional
from strawberry.types import Info

from .types import MediaType
from .resolvers import resolve_media


@strawberry.type
class MediaQuery:

    @strawberry.field(description="Fetch a media entity by any supported identifier")
    def media(
        self,
        info: Info,
        anilist: Optional[int] = strawberry.field(
            description="Anilist ID",
        ),
        mal: Optional[int] = strawberry.field(
            description="MyAnimeList ID",
        ),
        trakt: Optional[int] = strawberry.field(
            description="Trakt ID",
        ),
        slug: Optional[str] = strawberry.field(
            description="Series slug",
        ),
        tvdb: Optional[int] = strawberry.field(description="TVDB ID"),
        tmdb: Optional[int] = strawberry.field(description="TMDB ID"),
        notify: Optional[str] = strawberry.field(
            description="Notify.moe ID",
        ),
    ) -> Optional[MediaType]:
        return resolve_media(
            context=info.context,
            anilist=anilist,
            mal=mal,
            trakt=trakt,
            slug=slug,
            tvdb=tvdb,
            tmdb=tmdb,
            notify=notify,
        )

from typing import Annotated, Optional

import strawberry
from strawberry.types import Info

from episode.graphql.resolvers import resolve_episodes
from episode.graphql.types import EpisodeConnection


@strawberry.type
class EpisodeQuery:

    @strawberry.field(description="Paginated episodes by MyAnimeList ID")
    def episodes(
        self,
        info: Info,
        malId: Annotated[int, strawberry.argument(description="MyAnimeList ID")],
        limit: Optional[
            Annotated[int, strawberry.argument(description="Page size (1-100)")]
        ] = None,
        after: Optional[
            Annotated[str, strawberry.argument(description="Cursor for next page")]
        ] = None,
        before: Optional[
            Annotated[str, strawberry.argument(description="Cursor for previous page")]
        ] = None,
        kind: Optional[
            Annotated[str, strawberry.argument(description="Episode kind filter")]
        ] = None,
        specialsOnly: Optional[
            Annotated[bool, strawberry.argument(description="Filter specials only")]
        ] = None,
        start: Optional[
            Annotated[int, strawberry.argument(description="Filter start range")]
        ] = None,
        end: Optional[
            Annotated[int, strawberry.argument(description="Filter end range")]
        ] = None,
        includeOrphans: Optional[
            Annotated[
                bool,
                strawberry.argument(description="Include orphan episodes in results"),
            ]
        ] = None,
    ) -> EpisodeConnection:
        return resolve_episodes(
            context=info.context,
            mal_id=malId,
            limit=limit,
            after=after,
            before=before,
            kind=kind,
            specials_only=specialsOnly,
            start=start,
            end=end,
            include_orphans=includeOrphans,
        )

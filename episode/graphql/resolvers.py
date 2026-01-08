from typing import Optional

from strawberry.types.info import ContextType

from core.utilities import get_forwarded_headers
from episode.di.containers import EpisodeContainer
from episode.graphql.types import EpisodeConnection


def resolve_episodes(
    context: ContextType,
    mal_id: int,
    limit: Optional[int] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
    kind: Optional[str] = None,
    specials_only: Optional[bool] = None,
    start: Optional[int] = None,
    end: Optional[int] = None,
    include_orphans: Optional[bool] = None,
    use_case_provider=EpisodeContainer.use_case,
) -> EpisodeConnection:
    forwarded_headers = get_forwarded_headers(context)
    use_case = use_case_provider()
    response = use_case.fetch_episodes(
        mal_id=mal_id,
        headers=forwarded_headers,
        limit=limit,
        after=after,
        before=before,
        kind=kind,
        specials_only=specials_only,
        start=start,
        end=end,
        include_orphans=include_orphans,
    )
    return EpisodeConnection.from_model(response)

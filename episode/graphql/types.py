from typing import Optional, List
import strawberry

from core.graphql import EdgeImage, Instant


@strawberry.type
class EdgeStaff:
    creditId: str = strawberry.field(description="Credit ID for the crew member")
    id: int = strawberry.field(description="Unique ID for the crew member")
    knownFor: str = strawberry.field(
        description="Department the crew member is known for"
    )
    name: str = strawberry.field(description="Name of the crew member")
    originalName: str = strawberry.field(description="Original name of the crew member")
    popularity: float = strawberry.field(
        description="Popularity score of the crew member"
    )
    job: Optional[str] = strawberry.field(
        description="Job title of the crew member for this episode (e.g., Director, Writer)",
        default=None,
    )
    department: Optional[str] = strawberry.field(
        description="Department of the crew member (e.g., Directing, Writing)",
        default=None,
    )
    role: str = strawberry.field(
        description="Role of the crew member (e.g., CREW or GUEST)"
    )
    adult: Optional[bool] = strawberry.field(
        description="Indicates if the crew member is associated with adult content",
        default=None,
    )
    image: Optional[str] = strawberry.field(
        description="URL to an image of the crew member", default=None
    )
    character: Optional[str] = strawberry.field(
        description="Character name if the crew member is a voice actor/actress for this episode",
        default=None,
    )
    order: Optional[int] = strawberry.field(
        description="Order of appearance or importance", default=None
    )


@strawberry.type
class EdgeEpisode:
    id: int = strawberry.field(description="Unique ID for the episode")
    tvdbShowId: int = strawberry.field(
        description="TheTVDB Show ID this episode belongs to"
    )
    tvdbId: int = strawberry.field(description="TheTVDB Episode ID")
    seasonNumber: int = strawberry.field(
        description="Season number this episode belongs to"
    )
    episodeNumber: int = strawberry.field(
        description="Episode number within the season"
    )
    airDate: Instant = strawberry.field(description="Air date and time of the episode")
    staff: List[EdgeStaff] = strawberry.field(
        description="List of crew or guest members for this episode",
        default_factory=list,
    )
    absoluteEpisodeNumber: Optional[int] = strawberry.field(
        description="Absolute episode number across all seasons", default=None
    )
    airedBeforeSeasonNumber: Optional[int] = strawberry.field(
        description="If this episode aired before a specific season number",
        default=None,
    )
    airedBeforeEpisodeNumber: Optional[int] = strawberry.field(
        description="If this episode aired before a specific episode number (within airedBeforeSeasonNumber)",
        default=None,
    )
    airedAfterSeasonNumber: Optional[int] = strawberry.field(
        description="If this episode aired after a specific season number", default=None
    )
    airedAfterEpisodeNumber: Optional[int] = strawberry.field(
        description="If this episode aired after a specific episode number (within airedAfterSeasonNumber)",
        default=None,
    )
    title: Optional[str] = strawberry.field(
        description="Title of the episode", default=None
    )
    runtime: Optional[int] = strawberry.field(
        description="Runtime of the episode in minutes", default=None
    )
    overview: Optional[str] = strawberry.field(
        description="Brief overview or summary of the episode", default=None
    )
    image: Optional[str] = strawberry.field(
        description="URL to an image for the episode", default=None
    )
    name: Optional[str] = strawberry.field(
        description="Name of the episode (often same as title)", default=None
    )
    poster: Optional[str] = strawberry.field(
        description="URL to a poster image for the episode", default=None
    )


@strawberry.type
class EdgeSeason:
    tmdbId: int = strawberry.field(description="TheMovieDB ID for the season")
    airDate: Instant = strawberry.field(
        description="Air date of the first episode of the season"
    )
    episodeCount: int = strawberry.field(
        description="Number of episodes in this season"
    )
    name: str = strawberry.field(description="Name of the season")
    overview: str = strawberry.field(
        description="Brief overview or summary of the season"
    )
    number: int = strawberry.field(description="Season number")
    images: List[EdgeImage] = strawberry.field(
        description="Images associated with the season (posters, backdrops)"
    )
    cover: Optional[str] = strawberry.field(
        description="URL to a cover image for the season", default=None
    )
    episodes: List[EdgeEpisode] = strawberry.field(
        description="List of episodes in this season", default_factory=list
    )


@strawberry.type
class EpisodeObjectType:
    seasons: Optional[List[EdgeSeason]] = strawberry.field(
        description="List of seasons for the media, if applicable.",
        default_factory=list,
    )

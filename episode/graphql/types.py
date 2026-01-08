from enum import Enum
from typing import List, Optional

import strawberry

from core.graphql import Instant
from episode.data.schemas import Episode as EpisodeModel
from episode.data.schemas import EpisodeThemes as EpisodeThemesModel
from episode.data.schemas import EpisodeTitle as EpisodeTitleModel
from episode.data.schemas import EpisodesResponse


@strawberry.enum
class EpisodeKindEnum(str, Enum):
    main = "main"
    ova = "ova"
    ona = "ona"
    recap = "recap"
    filler = "filler"
    special = "special"


@strawberry.type
class EpisodeTitle:
    english: Optional[str] = strawberry.field(description="English title", default=None)
    romanji: Optional[str] = strawberry.field(description="Romanji title", default=None)
    native: Optional[str] = strawberry.field(description="Native title", default=None)

    @classmethod
    def from_model(cls, model: EpisodeTitleModel) -> "EpisodeTitle":
        return cls(english=model.english, romanji=model.romanji, native=model.native)


@strawberry.type
class EpisodeThemes:
    openings: List[str] = strawberry.field(
        description="Opening themes", default_factory=list
    )
    endings: List[str] = strawberry.field(
        description="Ending themes", default_factory=list
    )

    @classmethod
    def from_model(cls, model: EpisodeThemesModel) -> "EpisodeThemes":
        return cls(openings=model.openings, endings=model.endings)


@strawberry.type
class EpisodeType:
    id: int = strawberry.field(description="Unique ID for the episode")
    number: Optional[int] = strawberry.field(
        description="Episode number in listing", default=None
    )
    title: Optional[EpisodeTitle] = strawberry.field(
        description="Titles for the episode", default=None
    )
    synopsis: Optional[str] = strawberry.field(
        description="Episode synopsis", default=None
    )
    aired: Optional[Instant] = strawberry.field(
        description="Aired timestamp", default=None
    )
    score: Optional[float] = strawberry.field(description="Episode score", default=None)
    kind: Optional[EpisodeKindEnum] = strawberry.field(
        description="Episode type", default=None
    )
    duration: Optional[int] = strawberry.field(
        description="Runtime in minutes", default=None
    )
    url: Optional[str] = strawberry.field(description="Reference URL", default=None)
    tvdbShowId: Optional[int] = strawberry.field(
        description="TVDB show identifier", default=None
    )
    tvdbId: Optional[int] = strawberry.field(
        description="TVDB episode identifier", default=None
    )
    tmdbId: Optional[int] = strawberry.field(
        description="TMDB episode identifier", default=None
    )
    seasonNumber: Optional[int] = strawberry.field(
        description="Season number", default=None
    )
    episodeNumber: Optional[int] = strawberry.field(
        description="Episode number within season", default=None
    )
    absoluteEpisodeNumber: Optional[int] = strawberry.field(
        description="Absolute episode number", default=None
    )
    airedBeforeSeasonNumber: Optional[int] = strawberry.field(
        description="Season number the episode aired before", default=None
    )
    airedBeforeEpisodeNumber: Optional[int] = strawberry.field(
        description="Episode number the episode aired before", default=None
    )
    airedAfterSeasonNumber: Optional[int] = strawberry.field(
        description="Season number the episode aired after", default=None
    )
    airedAfterEpisodeNumber: Optional[int] = strawberry.field(
        description="Episode number the episode aired after", default=None
    )
    image: Optional[str] = strawberry.field(description="Episode image", default=None)
    poster: Optional[str] = strawberry.field(description="Episode poster", default=None)
    themes: EpisodeThemes = strawberry.field(
        description="Episode theme songs", default_factory=EpisodeThemes
    )

    @classmethod
    def from_model(cls, model: EpisodeModel) -> "EpisodeType":
        title = (
            EpisodeTitle.from_model(model.title) if model.title is not None else None
        )
        themes = (
            EpisodeThemes.from_model(model.themes)
            if model.themes is not None
            else EpisodeThemes()
        )
        return cls(
            id=model.id,
            number=model.number,
            title=title,
            synopsis=model.synopsis,
            aired=Instant(model.aired) if model.aired is not None else None,
            score=model.score,
            kind=EpisodeKindEnum(model.kind) if model.kind is not None else None,
            duration=model.duration,
            url=model.url,
            tvdbShowId=model.tvdbShowId,
            tvdbId=model.tvdbId,
            tmdbId=model.tmdbId,
            seasonNumber=model.seasonNumber,
            episodeNumber=model.episodeNumber,
            absoluteEpisodeNumber=model.absoluteEpisodeNumber,
            airedBeforeSeasonNumber=model.airedBeforeSeasonNumber,
            airedBeforeEpisodeNumber=model.airedBeforeEpisodeNumber,
            airedAfterSeasonNumber=model.airedAfterSeasonNumber,
            airedAfterEpisodeNumber=model.airedAfterEpisodeNumber,
            image=model.image,
            poster=model.poster,
            themes=themes,
        )


@strawberry.type
class EpisodeConnection:
    count: int = strawberry.field(description="Number of items returned")
    total: int = strawberry.field(description="Total items available")
    first: Optional[str] = strawberry.field(
        description="Cursor of first item", default=None
    )
    last: Optional[str] = strawberry.field(
        description="Cursor of last item", default=None
    )
    data: List[EpisodeType] = strawberry.field(description="Episode nodes")

    @classmethod
    def from_model(cls, model: EpisodesResponse) -> "EpisodeConnection":
        episodes = [EpisodeType.from_model(item) for item in model.data]
        return cls(
            count=model.count,
            total=model.total,
            first=model.first,
            last=model.last,
            data=episodes,
        )

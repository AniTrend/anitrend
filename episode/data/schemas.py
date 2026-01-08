from dataclasses import dataclass, field
from typing import List, Literal, Optional

EpisodeKind = Literal["main", "ova", "ona", "recap", "filler", "special"]

ALLOW_NONE_REQUIRED = {"required": True, "allow_none": True}


@dataclass
class EpisodeTitle:
    english: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    romanji: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    native: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)


@dataclass
class EpisodeThemes:
    openings: List[str] = field(default_factory=list, metadata={"required": True})
    endings: List[str] = field(default_factory=list, metadata={"required": True})


@dataclass
class Episode:
    id: int
    number: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    title: Optional[EpisodeTitle] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    synopsis: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    aired: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    score: Optional[float] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    kind: Optional[EpisodeKind] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    duration: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    url: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    tvdbShowId: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    tvdbId: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    tmdbId: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    seasonNumber: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    episodeNumber: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    absoluteEpisodeNumber: Optional[int] = field(
        default=None, metadata=ALLOW_NONE_REQUIRED
    )
    airedBeforeSeasonNumber: Optional[int] = field(
        default=None, metadata=ALLOW_NONE_REQUIRED
    )
    airedBeforeEpisodeNumber: Optional[int] = field(
        default=None, metadata=ALLOW_NONE_REQUIRED
    )
    airedAfterSeasonNumber: Optional[int] = field(
        default=None, metadata=ALLOW_NONE_REQUIRED
    )
    airedAfterEpisodeNumber: Optional[int] = field(
        default=None, metadata=ALLOW_NONE_REQUIRED
    )
    image: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    poster: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    themes: EpisodeThemes = field(
        default_factory=EpisodeThemes, metadata={"required": True}
    )


@dataclass
class EpisodesResponse:
    data: List[Episode] = field(default_factory=list, metadata={"required": True})
    first: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    last: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    count: int = field(default=0)
    total: int = field(default=0)
    message: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    errors: Optional[List[str]] = field(default=None, metadata=ALLOW_NONE_REQUIRED)

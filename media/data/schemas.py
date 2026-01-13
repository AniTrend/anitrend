from dataclasses import dataclass, field
from typing import List, Literal, Optional

MediaKind = Literal["ANIME", "MANGA"]
ImageType = Literal["BACKDROP", "POSTER", "LOGO"]
NetworkCategory = Literal["DISTRIBUTION", "PRODUCTION"]

ANIME_MEDIA_KIND: MediaKind = "ANIME"
ALLOW_NONE_REQUIRED = {"required": True, "allow_none": True}


@dataclass
class SeriesId:
    anidb: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    anilist: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    animePlanet: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    anisearch: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    imdb: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    kitsu: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    livechart: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    notify: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    themoviedb: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    tvdb: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    myanimelist: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    tvMazeId: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    tvrage: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    slug: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    shoboi: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    trakt: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)


@dataclass
class SeriesTitle:
    english: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    canonical: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    harigana: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    japanese: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    romaji: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    synonyms: Optional[List[str]] = field(default=None, metadata=ALLOW_NONE_REQUIRED)


@dataclass
class SeriesScheduleEpisode:
    id: int
    name: str
    overview: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    airDate: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    episodeNumber: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    productionCode: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    runtime: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    seasonNumber: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    tmdbId: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    image: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)


@dataclass
class SeriesSchedule:
    firstAirDate: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    lastAirDate: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    lastAiredEpisode: Optional[SeriesScheduleEpisode] = field(
        default=None, metadata=ALLOW_NONE_REQUIRED
    )
    nextEpisodeToAir: Optional[SeriesScheduleEpisode] = field(
        default=None, metadata=ALLOW_NONE_REQUIRED
    )


@dataclass
class SeriesNetwork:
    id: int
    name: str
    originCountry: str
    category: NetworkCategory
    isPrimary: bool
    logoPath: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)


@dataclass
class SeriesImageAttributes:
    url: str
    height: int
    width: int
    type: ImageType
    locale: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)


@dataclass
class SeriesTrailer:
    id: str
    site: str
    thumbnail: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)


@dataclass
class SeriesCoverImage:
    extraLarge: Optional[str] = None
    large: Optional[str] = None
    medium: Optional[str] = None
    color: Optional[str] = None


@dataclass
class AnimeThemeMeta:
    type: Literal["OP", "ED"]
    number: int
    version: int


@dataclass
class AnimeTheme:
    id: str
    name: str
    video: str
    meta: AnimeThemeMeta
    audio: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)


@dataclass
class MangaMetadata:
    chapters: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    volumes: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    publishedFrom: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    publishedTo: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)


@dataclass
class MediaEntity:
    id: str
    kind: MediaKind
    mediaId: SeriesId
    cover: SeriesCoverImage
    title: SeriesTitle
    updatedAt: int
    classification: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    images: List[SeriesImageAttributes] = field(
        default_factory=list, metadata={"required": True}
    )
    banner: Optional[str] = None
    fanart: Optional[str] = None
    format: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    ageRating: Optional[str] = None
    description: Optional[str] = None
    moreInfo: Optional[str] = None
    duration: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    themeSongs: List[AnimeTheme] = field(
        default_factory=list, metadata={"required": True}
    )
    schedule: Optional[SeriesSchedule] = field(
        default=None, metadata=ALLOW_NONE_REQUIRED
    )
    trailers: List[SeriesTrailer] = field(
        default_factory=list, metadata={"required": True}
    )
    networks: List[SeriesNetwork] = field(
        default_factory=list, metadata={"required": True}
    )
    airedEpisodes: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    broadcast: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    isAdult: Optional[bool] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    homepage: Optional[str] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    chapters: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    volumes: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    publishedFrom: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
    publishedTo: Optional[int] = field(default=None, metadata=ALLOW_NONE_REQUIRED)
# Backwards compatibility: existing imports expecting `Media` should continue to work.
Media = MediaEntity

from dataclasses import dataclass, field
from typing import List, Literal, Optional

MediaKind = Literal["ANIME", "MANGA"]
ImageType = Literal["BACKDROP", "POSTER", "LOGO"]
NetworkCategory = Literal["DISTRIBUTION", "PRODUCTION"]

ANIME_MEDIA_KIND: MediaKind = "ANIME"
ALLOW_NONE_REQUIRED = {"required": True, "allow_none": True}
ALLOW_NONE_OPTIONAL = {"required": False, "allow_none": True}


@dataclass
class SeriesId:
    anidb: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    anilist: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    animePlanet: Optional[str] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    anisearch: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    imdb: Optional[str] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    kitsu: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    livechart: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    notify: Optional[str] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    themoviedb: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    tvdb: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    myanimelist: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    tvMazeId: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    tvrage: Optional[str] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    slug: Optional[str] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    shoboi: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    trakt: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)


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
    overview: Optional[str] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    airDate: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    episodeNumber: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    productionCode: Optional[str] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    runtime: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    seasonNumber: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    tmdbId: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    image: Optional[str] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)


@dataclass
class SeriesSchedule:
    firstAirDate: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    lastAirDate: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    lastAiredEpisode: Optional[SeriesScheduleEpisode] = field(
        default=None, metadata=ALLOW_NONE_OPTIONAL
    )
    nextEpisodeToAir: Optional[SeriesScheduleEpisode] = field(
        default=None, metadata=ALLOW_NONE_OPTIONAL
    )


@dataclass
class SeriesNetwork:
    id: int
    name: str
    originCountry: str
    category: NetworkCategory
    isPrimary: bool
    logoPath: Optional[str] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)


@dataclass
class SeriesImageAttributes:
    url: str
    height: int
    width: int
    type: ImageType
    locale: Optional[str] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)


@dataclass
class SeriesTrailer:
    id: str
    site: str
    thumbnail: Optional[str] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)


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
    audio: Optional[str] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)


@dataclass
class MangaMetadata:
    chapters: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    volumes: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    publishedFrom: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    publishedTo: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)


@dataclass
class MediaEntity:
    id: str
    kind: MediaKind
    mediaId: SeriesId
    cover: SeriesCoverImage
    title: SeriesTitle
    updatedAt: int
    classification: Optional[str] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
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
    duration: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    themeSongs: List[AnimeTheme] = field(
        default_factory=list, metadata={"required": True}
    )
    schedule: Optional[SeriesSchedule] = field(
        default=None, metadata=ALLOW_NONE_OPTIONAL
    )
    trailers: List[SeriesTrailer] = field(
        default_factory=list, metadata={"required": True}
    )
    networks: List[SeriesNetwork] = field(
        default_factory=list, metadata={"required": True}
    )
    airedEpisodes: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    broadcast: Optional[str] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    isAdult: Optional[bool] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    homepage: Optional[str] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    chapters: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    volumes: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    publishedFrom: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)
    publishedTo: Optional[int] = field(default=None, metadata=ALLOW_NONE_OPTIONAL)


# Backwards compatibility: existing imports expecting `Media` should continue to work.
Media = MediaEntity

from dataclasses import dataclass, field
from typing import List, Literal, Optional

MediaKind = Literal["ANIME", "MANGA"]
ImageType = Literal["BACKDROP", "POSTER", "LOGO"]
NetworkCategory = Literal["DISTRIBUTION", "PRODUCTION"]

ANIME_MEDIA_KIND: MediaKind = "ANIME"


@dataclass
class SeriesId:
    anidb: Optional[int] = None
    anilist: Optional[int] = None
    animePlanet: Optional[str] = None
    anisearch: Optional[int] = None
    imdb: Optional[str] = None
    kitsu: Optional[int] = None
    livechart: Optional[int] = None
    notify: Optional[str] = None
    themoviedb: Optional[int] = None
    tvdb: Optional[int] = None
    myanimelist: Optional[int] = None
    tvMazeId: Optional[int] = None
    tvrage: Optional[str] = None
    slug: Optional[str] = None
    shoboi: Optional[int] = None
    trakt: Optional[int] = None


@dataclass
class SeriesTitle:
    english: Optional[str] = None
    canonical: Optional[str] = None
    harigana: Optional[str] = None
    japanese: Optional[str] = None
    romaji: Optional[str] = None
    synonyms: Optional[List[str]] = None


@dataclass
class SeriesScheduleEpisode:
    id: int
    name: str
    overview: str
    airDate: int
    episodeNumber: int
    productionCode: str
    runtime: int
    seasonNumber: int
    tmdbId: int
    image: Optional[str] = None


@dataclass
class SeriesSchedule:
    firstAirDate: Optional[int] = None
    lastAirDate: Optional[int] = None
    lastAiredEpisode: Optional[SeriesScheduleEpisode] = None
    nextEpisodeToAir: Optional[SeriesScheduleEpisode] = None


@dataclass
class SeriesNetwork:
    id: int
    name: str
    originCountry: str
    category: NetworkCategory
    isPrimary: bool
    logoPath: Optional[str] = None


@dataclass
class SeriesImageAttributes:
    url: str
    height: int
    width: int
    type: ImageType
    locale: Optional[str] = None


@dataclass
class SeriesTrailer:
    id: str
    site: str
    thumbnail: Optional[str] = None


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
    audio: Optional[str] = None


@dataclass
class MangaMetadata:
    chapters: Optional[int] = None
    volumes: Optional[int] = None
    publishedFrom: Optional[int] = None
    publishedTo: Optional[int] = None


@dataclass
class MediaEntity:
    id: str
    kind: MediaKind
    mediaId: SeriesId
    cover: SeriesCoverImage
    title: SeriesTitle
    updatedAt: int
    images: List[SeriesImageAttributes] = field(default_factory=list)
    banner: Optional[str] = None
    fanart: Optional[str] = None
    format: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    ageRating: Optional[str] = None
    description: Optional[str] = None
    moreInfo: Optional[str] = None
    themeSongs: List[AnimeTheme] = field(default_factory=list)
    schedule: Optional[SeriesSchedule] = None
    trailers: List[SeriesTrailer] = field(default_factory=list)
    networks: List[SeriesNetwork] = field(default_factory=list)
    airedEpisodes: Optional[int] = None
    broadcast: Optional[str] = None
    isAdult: Optional[bool] = None
    homepage: Optional[str] = None
    chapters: Optional[int] = None
    volumes: Optional[int] = None
    publishedFrom: Optional[int] = None
    publishedTo: Optional[int] = None


# Backwards compatibility: existing imports expecting `Media` should continue to work.
Media = MediaEntity

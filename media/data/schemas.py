from dataclasses import dataclass, field
from typing import List, Literal, Optional

# Based on https://github.com/AniTrend/on-the-edge/blob/dev/src/series/types.ts


# Corresponds to SeriesId in types.ts
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
    shoboi: Optional[int] = None  # Note: shoboi is not optional in TS, adjust if needed
    trakt: Optional[int] = None


# Corresponds to SeriesTitle in types.ts
@dataclass
class SeriesTitle:
    english: Optional[str] = None
    canonical: Optional[str] = None
    harigana: Optional[str] = None  # Assuming typo in TS, should be hiragana?
    japanese: Optional[str] = None
    romaji: Optional[str] = None
    synonyms: Optional[List[str]] = field(default_factory=list)


# Corresponds to SeriesScheduleEpisode in types.ts
@dataclass
class SeriesScheduleEpisode:
    id: int
    name: str
    overview: str
    airDate: int
    episodeNumber: int
    productionCode: str
    seasonNumber: int
    tmdbId: int
    runtime: Optional[int] = None
    image: Optional[str] = None


# Corresponds to SeriesSchedule in types.ts
@dataclass
class SeriesSchedule:
    firstAirDate: int
    lastAirDate: int
    lastAiredEpisode: Optional[SeriesScheduleEpisode] = None
    nextEpisodeToAir: Optional[SeriesScheduleEpisode] = None


# Corresponds to SeriesNetwork in types.ts
@dataclass
class SeriesNetwork:
    id: int
    isPrimary: bool
    name: str
    originCountry: str
    category: Literal[
        "DISTRIBUTION", "PRODUCTION"
    ]  # Literal['DISTRIBUTION', 'PRODUCTION'] if stricter typing needed
    logoPath: Optional[str] = None


# Corresponds to SeriesImageBackdrop in types.ts
@dataclass
class SeriesImageBackdrop:
    height: Optional[int] = None
    width: Optional[int] = None
    url: Optional[str] = None
    locale: Optional[str] = None


# Corresponds to SeriesImage in types.ts
@dataclass
class SeriesImage:
    backdrops: List[SeriesImageBackdrop] = field(default_factory=list)
    logos: List[SeriesImageBackdrop] = field(default_factory=list)
    posters: List[SeriesImageBackdrop] = field(default_factory=list)


# Corresponds to SeriesEpisodeCrew in types.ts
@dataclass
class SeriesEpisodeCrew:
    creditId: str
    id: int
    knownFor: str  # known_for_department in TMDB?
    name: str
    originalName: str
    popularity: float  # number maps to float usually
    job: Optional[str] = None
    department: Optional[str] = None
    adult: Optional[bool] = None
    image: Optional[str] = None
    character: Optional[str] = None
    order: Optional[int] = None


# Corresponds to SeriesEpisode in types.ts
@dataclass
class SeriesEpisode:
    id: int
    tvdbShowId: int
    tvdbId: int
    seasonNumber: int
    episodeNumber: int
    airDate: int
    crew: List[SeriesEpisodeCrew] = field(default_factory=list)
    guests: List[SeriesEpisodeCrew] = field(
        default_factory=list
    )  # Assuming guests have same structure
    absoluteEpisodeNumber: Optional[int] = None
    airedBeforeSeasonNumber: Optional[int] = None
    airedBeforeEpisodeNumber: Optional[int] = None
    airedAfterSeasonNumber: Optional[int] = None
    airedAfterEpisodeNumber: Optional[int] = None
    title: Optional[str] = None
    runtime: Optional[int] = None
    overview: Optional[str] = None
    image: Optional[str] = None
    name: Optional[str] = None  # Duplicate of title? Check usage
    poster: Optional[str] = None


# Corresponds to SeriesSeason in types.ts
@dataclass
class SeriesSeason:
    tmdbId: int
    airDate: int
    episodeCount: int
    name: str
    overview: str
    number: int  # season_number
    image: SeriesImage
    episodes: List[SeriesEpisode] = field(default_factory=list)
    cover: Optional[str] = None


# Corresponds to SeriesTrailer in types.ts
@dataclass
class SeriesTrailer:
    id: str
    site: str
    thumbnail: Optional[str] = None


# Corresponds to SeriesCoverImage in types.ts
@dataclass
class SeriesCoverImage:
    extraLarge: Optional[str] = None
    large: Optional[str] = None
    medium: Optional[str] = None
    color: Optional[str] = None


# Corresponds to AnimeTheme meta in types.ts
@dataclass
class AnimeThemeMeta:
    type: Literal["OP", "ED"]  # ThemeType -> OPENING | ENDING
    number: int
    version: int


# Corresponds to AnimeTheme in types.ts
@dataclass
class AnimeTheme:
    id: str
    name: str
    video: str
    meta: AnimeThemeMeta
    audio: Optional[str] = None


# Corresponds to Media interface in types.ts
@dataclass
class Media:
    id: str
    mediaId: SeriesId
    cover: SeriesCoverImage
    title: SeriesTitle
    image: SeriesImage  # This holds backdrops, logos, posters
    updatedAt: int
    banner: Optional[str] = None
    fanart: Optional[str] = None
    format: Optional[Literal["TV", "MOVIE", "SPECIAL", "OVA", "ONA"]] = None
    status: Optional[Literal["FINISHED", "RELEASING", "NOT_YET_RELEASED"]] = None
    source: Optional[
        Literal[
            "ORIGINAL", "MANGA", "LIGHT_NOVEL", "VISUAL_NOVEL", "VIDEO_GAME", "OTHER"
        ]
    ] = None
    themeSongs: List[AnimeTheme] = field(default_factory=list)
    schedule: Optional[SeriesSchedule] = None
    ageRating: Optional[str] = None
    isAdult: Optional[bool] = None
    trailers: List[SeriesTrailer] = field(default_factory=list)
    networks: List[SeriesNetwork] = field(default_factory=list)
    homepage: Optional[str] = None
    description: Optional[str] = None
    airedEpisodes: Optional[int] = None
    seasons: List[SeriesSeason] = field(default_factory=list)


@dataclass
class MediaApiResponse:
    data: Optional[Media] = None
    message: Optional[str] = None

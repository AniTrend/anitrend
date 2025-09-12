import strawberry
from typing import List, Optional

from core.graphql.types import Instant

# Based on media/data/schemas.py which is based on on-the-edge/src/series/types.ts


@strawberry.type
class SeriesIdType:
    anidb: Optional[int] = strawberry.field(description="AniDB ID", default=None)
    anilist: Optional[int] = strawberry.field(description="Anilist ID", default=None)
    animePlanet: Optional[str] = strawberry.field(
        description="Anime-Planet ID or slug", default=None
    )
    anisearch: Optional[int] = strawberry.field(
        description="Anisearch ID", default=None
    )
    imdb: Optional[str] = strawberry.field(description="IMDb ID", default=None)
    kitsu: Optional[int] = strawberry.field(description="Kitsu ID", default=None)
    livechart: Optional[int] = strawberry.field(
        description="LiveChart ID", default=None
    )
    notify: Optional[str] = strawberry.field(description="Notify.moe ID", default=None)
    themoviedb: Optional[int] = strawberry.field(
        description="TheMovieDB ID", default=None
    )
    tvdb: Optional[int] = strawberry.field(description="TheTVDB ID", default=None)
    myanimelist: Optional[int] = strawberry.field(
        description="MyAnimeList ID", default=None
    )
    tvMazeId: Optional[int] = strawberry.field(description="TVMaze ID", default=None)
    tvrage: Optional[str] = strawberry.field(description="TVRage ID", default=None)
    slug: Optional[str] = strawberry.field(description="Series slug", default=None)
    shoboi: Optional[int] = strawberry.field(
        description="Shoboi Calendar ID", default=None
    )
    trakt: Optional[int] = strawberry.field(description="Trakt ID", default=None)


@strawberry.type
class SeriesTitleType:
    english: Optional[str] = strawberry.field(description="English title", default=None)
    canonical: Optional[str] = strawberry.field(
        description="Canonical title", default=None
    )
    harigana: Optional[str] = strawberry.field(
        description="Hiragana title (Note: source field name was 'harigana')",
        default=None,
    )
    japanese: Optional[str] = strawberry.field(
        description="Japanese title", default=None
    )
    romaji: Optional[str] = strawberry.field(description="Romaji title", default=None)
    synonyms: Optional[List[str]] = strawberry.field(
        description="List of alternative titles or synonyms", default_factory=list
    )


@strawberry.type
class SeriesScheduleEpisodeType:
    id: int = strawberry.field(description="Unique ID for the scheduled episode")
    name: str = strawberry.field(description="Name or title of the episode")
    overview: str = strawberry.field(
        description="Brief overview or summary of the episode"
    )
    airDate: Instant = strawberry.field(description="Air date and time of the episode")
    episodeNumber: int = strawberry.field(description="Episode number in the season")
    productionCode: str = strawberry.field(description="Production code of the episode")
    runtime: int = strawberry.field(description="Runtime of the episode in minutes")
    seasonNumber: int = strawberry.field(
        description="Season number this episode belongs to"
    )
    tmdbId: int = strawberry.field(description="TheMovieDB ID for the episode")
    image: Optional[str] = strawberry.field(
        description="URL to an image for the episode", default=None
    )


@strawberry.type
class SeriesScheduleType:
    firstAirDate: Instant = strawberry.field(description="First air date of the series")
    lastAirDate: Instant = strawberry.field(description="Last air date of the series")
    lastAiredEpisode: Optional[SeriesScheduleEpisodeType] = strawberry.field(
        description="Details of the last aired episode", default=None
    )
    nextEpisodeToAir: Optional[SeriesScheduleEpisodeType] = strawberry.field(
        description="Details of the next episode to air", default=None
    )


@strawberry.type
class SeriesNetworkType:
    id: int = strawberry.field(description="Unique ID for the network")
    isPrimary: bool = strawberry.field(
        description="Indicates if this is the primary network"
    )
    name: str = strawberry.field(description="Name of the network")
    originCountry: str = strawberry.field(description="Origin country of the network")
    category: str = strawberry.field(
        description="Category of the network (e.g., DISTRIBUTION, PRODUCTION)"
    )
    logoPath: Optional[str] = strawberry.field(
        description="Path or URL to the network's logo", default=None
    )


@strawberry.type
class SeriesImageType:
    height: int = strawberry.field(description="Height of the image in pixels")
    width: int = strawberry.field(description="Width of the image in pixels")
    url: str = strawberry.field(description="URL to the image")
    locale: Optional[str] = strawberry.field(
        description="Locale of the image (e.g., en, ja)", default=None
    )
    type: str = strawberry.field(
        description="Type of the image (e.g., BACKDROP, LOGO, POSTER)"
    )


@strawberry.type
class SeriesSeasonType:
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
    images: List[SeriesImageType] = strawberry.field(
        description="Images associated with the season (posters, backdrops)"
    )
    cover: Optional[str] = strawberry.field(
        description="URL to a cover image for the season", default=None
    )


@strawberry.type
class SeriesTrailerType:
    id: str = strawberry.field(
        description="Unique ID for the trailer (e.g., YouTube video ID)"
    )
    site: str = strawberry.field(
        description="Site where the trailer is hosted (e.g., YouTube)"
    )
    thumbnail: Optional[str] = strawberry.field(
        description="URL to a thumbnail image for the trailer", default=None
    )


@strawberry.type
class SeriesCoverImageType:
    extraLarge: Optional[str] = strawberry.field(
        description="URL to an extra large cover image", default=None
    )
    large: Optional[str] = strawberry.field(
        description="URL to a large cover image", default=None
    )
    medium: Optional[str] = strawberry.field(
        description="URL to a medium cover image", default=None
    )
    color: Optional[str] = strawberry.field(
        description="Dominant color of the cover image (hex code)", default=None
    )


@strawberry.type
class AnimeThemeMetaType:
    type: str = strawberry.field(
        description="Type of the theme song (e.g., OPENING, ENDING)"
    )
    number: int = strawberry.field(
        description="Sequence number of the theme (e.g., 1 for OP1, 2 for OP2)"
    )
    version: int = strawberry.field(
        description="Version number of the theme (e.g., for themes with multiple visual versions)"
    )


@strawberry.type
class AnimeThemeType:
    id: str = strawberry.field(description="Unique ID for the anime theme song")
    name: str = strawberry.field(description="Name or title of the theme song")
    video: str = strawberry.field(description="URL to the video of the theme song")
    meta: AnimeThemeMetaType = strawberry.field(
        description="Metadata about the theme song (type, number, version)"
    )
    audio: Optional[str] = strawberry.field(
        description="URL to the audio of the theme song", default=None
    )


@strawberry.type
class MediaType:  # Corresponds to Media dataclass from schemas.py
    id: str = strawberry.field(
        description="The unique identifier for the media entity (often corresponds to 'notify' ID or a combined key)."
    )
    mediaId: SeriesIdType = strawberry.field(
        description="A collection of alternative identifiers for the media from various sources."
    )
    cover: SeriesCoverImageType = strawberry.field(
        description="Cover images for the media (extraLarge, large, medium, color)."
    )
    title: SeriesTitleType = strawberry.field(
        description="Titles of the media in various languages (english, romaji, native, etc.)."
    )
    image: SeriesImageType = strawberry.field(
        description="Collection of images for the media (backdrops, logos, posters)."
    )
    updatedAt: Instant = strawberry.field(
        description="Timestamp of when the media information was last updated."
    )
    banner: Optional[str] = strawberry.field(
        description="URL to a banner image for the media.", default=None
    )
    fanart: Optional[str] = strawberry.field(
        description="URL to a fanart image for the media.", default=None
    )
    format: Optional[str] = strawberry.field(
        description="Format of the media (e.g., TV, MOVIE, OVA, ONA, MANGA).",
        default=None,
    )
    status: Optional[str] = strawberry.field(
        description="Current status of the media (e.g., RELEASING, FINISHED, NOT_YET_RELEASED, CANCELLED).",
        default=None,
    )
    source: Optional[str] = strawberry.field(
        description="Source material of the media (e.g., ORIGINAL, MANGA, LIGHT_NOVEL, GAME).",
        default=None,
    )
    themeSongs: List[AnimeThemeType] = strawberry.field(
        description="List of theme songs (openings and endings).", default_factory=list
    )
    schedule: Optional[SeriesScheduleType] = strawberry.field(
        description="Airing schedule information for the media.", default=None
    )
    ageRating: Optional[str] = strawberry.field(
        description="Age rating of the media (e.g., G, PG, R17).", default=None
    )
    isAdult: Optional[bool] = strawberry.field(
        description="Indicates if the media is considered adult content.", default=None
    )
    trailers: List[SeriesTrailerType] = strawberry.field(
        description="List of trailers for the media.", default_factory=list
    )
    networks: List[SeriesNetworkType] = strawberry.field(
        description="List of networks associated with the media.", default_factory=list
    )
    homepage: Optional[str] = strawberry.field(
        description="URL to the official homepage of the media.", default=None
    )
    description: Optional[str] = strawberry.field(
        description="Synopsis or description of the media.", default=None
    )
    airedEpisodes: Optional[int] = strawberry.field(
        description="Total number of aired episodes.", default=None
    )
    seasons: Optional[List[SeriesSeasonType]] = strawberry.field(
        description="List of seasons for the media, if applicable.",
        default_factory=list,
    )

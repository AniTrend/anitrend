import strawberry
from typing import List, Optional

from core.graphql import EdgeImage, Instant


@strawberry.type
class EdgeMediaId:
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
class EdgeMediaTitle:
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
class EdgeMediaEpisode:
    id: int = strawberry.field(description="Unique ID for the scheduled episode")
    name: Optional[str] = strawberry.field(
        description="Name or title of the episode", default=None
    )
    overview: Optional[str] = strawberry.field(
        description="Brief overview or summary of the episode", default=None
    )
    airDate: Optional[Instant] = strawberry.field(
        description="Air date and time of the episode", default=None
    )
    episodeNumber: Optional[int] = strawberry.field(
        description="Episode number in the season", default=None
    )
    productionCode: Optional[str] = strawberry.field(
        description="Production code of the episode", default=None
    )
    runtime: Optional[int] = strawberry.field(
        description="Runtime of the episode in minutes", default=None
    )
    seasonNumber: Optional[int] = strawberry.field(
        description="Season number this episode belongs to", default=None
    )
    tmdbId: Optional[int] = strawberry.field(
        description="TheMovieDB ID for the episode", default=None
    )
    image: Optional[str] = strawberry.field(
        description="URL to an image for the episode", default=None
    )


@strawberry.type
class EdgeAiringSchedule:
    firstAirDate: Optional[Instant] = strawberry.field(
        description="First air date of the series", default=None
    )
    lastAirDate: Optional[Instant] = strawberry.field(
        description="Last air date of the series", default=None
    )
    lastAiredEpisode: Optional[EdgeMediaEpisode] = strawberry.field(
        description="Details of the last aired episode", default=None
    )
    nextEpisodeToAir: Optional[EdgeMediaEpisode] = strawberry.field(
        description="Details of the next episode to air", default=None
    )


@strawberry.type
class EdgeMediaNetwork:
    id: int = strawberry.field(description="Unique ID for the network")
    isPrimary: Optional[bool] = strawberry.field(
        description="Indicates if this is the primary network", default=None
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
class EdgeMediaTrailer:
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
class EdgeCoverImage:
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
class EdgeMediaTheme:
    id: str = strawberry.field(description="Unique ID for the anime theme song")
    name: str = strawberry.field(description="Name or title of the theme song")
    video: str = strawberry.field(description="URL to the video of the theme song")
    meta: Optional["EdgeMediaThemeMeta"] = strawberry.field(
        description="Metadata about the theme song, including type, number, and version.",
        default=None,
    )
    audio: Optional[str] = strawberry.field(
        description="URL to the audio track of the theme song", default=None
    )


@strawberry.type
class EdgeMediaThemeMeta:
    type: str = strawberry.field(
        description="Type of the theme song (e.g., OP for opening, ED for ending)"
    )
    number: int = strawberry.field(
        description="Sequence number of the theme (e.g., 1 for OP1, 2 for OP2)"
    )
    version: int = strawberry.field(
        description="Version number of the theme (e.g., for themes with multiple visual versions)"
    )


@strawberry.type
class MediaType:
    id: str = strawberry.field(
        description="The unique identifier for the media entity (often corresponds to the Notify.moe edge ID)."
    )
    kind: str = strawberry.field(
        description="The kind of media entity (e.g., ANIME, MANGA)."
    )
    mediaId: EdgeMediaId = strawberry.field(
        description="A collection of alternative identifiers for the media from various sources."
    )
    cover: EdgeCoverImage = strawberry.field(
        description="Cover images for the media (extraLarge, large, medium, color)."
    )
    title: EdgeMediaTitle = strawberry.field(
        description="Titles of the media in various languages (english, romaji, native, etc.)."
    )
    updatedAt: Instant = strawberry.field(
        description="Timestamp of when the media information was last updated."
    )
    images: List[EdgeImage] = strawberry.field(
        description="Gallery of images related to the media (posters, backdrops, logos).",
        default_factory=list,
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
        description="Current status of the media (e.g., RELEASING, FINISHED, NOT_YET_RELEASED).",
        default=None,
    )
    source: Optional[str] = strawberry.field(
        description="Source material of the media (e.g., ORIGINAL, MANGA, LIGHT_NOVEL, GAME).",
        default=None,
    )
    ageRating: Optional[str] = strawberry.field(
        description="Age rating of the media (e.g., G, PG, R17).", default=None
    )
    description: Optional[str] = strawberry.field(
        description="Synopsis or description of the media.", default=None
    )
    moreInfo: Optional[str] = strawberry.field(
        description="Link to additional information about the media.", default=None
    )
    themeSongs: List[EdgeMediaTheme] = strawberry.field(
        description="List of theme songs (openings and endings).", default_factory=list
    )
    schedule: Optional[EdgeAiringSchedule] = strawberry.field(
        description="Airing schedule information for the media.", default=None
    )
    trailers: List[EdgeMediaTrailer] = strawberry.field(
        description="List of trailers for the media.", default_factory=list
    )
    networks: List[EdgeMediaNetwork] = strawberry.field(
        description="List of networks associated with the media.", default_factory=list
    )
    airedEpisodes: Optional[int] = strawberry.field(
        description="Total number of aired episodes.", default=None
    )
    broadcast: Optional[str] = strawberry.field(
        description="Broadcast schedule information (e.g., day and time).",
        default=None,
    )
    isAdult: Optional[bool] = strawberry.field(
        description="Indicates if the media is considered adult content.", default=None
    )
    homepage: Optional[str] = strawberry.field(
        description="URL to the official homepage of the media.", default=None
    )
    chapters: Optional[int] = strawberry.field(
        description="Total number of chapters (for manga).", default=None
    )
    volumes: Optional[int] = strawberry.field(
        description="Total number of volumes (for manga).", default=None
    )
    publishedFrom: Optional[Instant] = strawberry.field(
        description="Publication start date (for manga).", default=None
    )
    publishedTo: Optional[Instant] = strawberry.field(
        description="Publication end date (for manga).", default=None
    )

from enum import Enum
from typing import List, Optional

import strawberry

from core.graphql import EdgeImage, Instant
from media.data.schemas import (
    AnimeTheme,
    AnimeThemeMeta,
    MediaEntity,
    SeriesCoverImage,
    SeriesId,
    SeriesNetwork,
    SeriesSchedule,
    SeriesScheduleEpisode,
    SeriesTitle,
    SeriesTrailer,
)


@strawberry.enum
class MediaKindEnum(str, Enum):
    ANIME = "ANIME"
    MANGA = "MANGA"


@strawberry.enum
class NetworkCategoryEnum(str, Enum):
    DISTRIBUTION = "DISTRIBUTION"
    PRODUCTION = "PRODUCTION"


@strawberry.enum
class ThemeSongTypeEnum(str, Enum):
    OP = "OP"
    ED = "ED"


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

    @classmethod
    def from_model(cls, model: SeriesId) -> "EdgeMediaId":
        return cls(
            anidb=model.anidb,
            anilist=model.anilist,
            animePlanet=model.animePlanet,
            anisearch=model.anisearch,
            imdb=model.imdb,
            kitsu=model.kitsu,
            livechart=model.livechart,
            notify=model.notify,
            themoviedb=model.themoviedb,
            tvdb=model.tvdb,
            myanimelist=model.myanimelist,
            tvMazeId=model.tvMazeId,
            tvrage=model.tvrage,
            slug=model.slug,
            shoboi=model.shoboi,
            trakt=model.trakt,
        )


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
        description="List of alternative titles or synonyms", default=None
    )

    @classmethod
    def from_model(cls, model: SeriesTitle) -> "EdgeMediaTitle":
        return cls(
            english=model.english,
            canonical=model.canonical,
            harigana=model.harigana,
            japanese=model.japanese,
            romaji=model.romaji,
            synonyms=model.synonyms,
        )


@strawberry.type
class EdgeMediaEpisode:
    id: int = strawberry.field(description="Unique ID for the scheduled episode")
    name: str = strawberry.field(description="Name or title of the episode")
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

    @classmethod
    def from_model(cls, model: SeriesScheduleEpisode) -> "EdgeMediaEpisode":
        return cls(
            id=model.id,
            name=model.name,
            overview=model.overview,
            airDate=(Instant(model.airDate) if model.airDate is not None else None),
            episodeNumber=model.episodeNumber,
            productionCode=model.productionCode,
            runtime=model.runtime,
            seasonNumber=model.seasonNumber,
            tmdbId=model.tmdbId,
            image=model.image,
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

    @classmethod
    def from_model(cls, model: SeriesSchedule) -> "EdgeAiringSchedule":
        return cls(
            firstAirDate=(
                Instant(model.firstAirDate) if model.firstAirDate is not None else None
            ),
            lastAirDate=(
                Instant(model.lastAirDate) if model.lastAirDate is not None else None
            ),
            lastAiredEpisode=(
                EdgeMediaEpisode.from_model(model.lastAiredEpisode)
                if model.lastAiredEpisode is not None
                else None
            ),
            nextEpisodeToAir=(
                EdgeMediaEpisode.from_model(model.nextEpisodeToAir)
                if model.nextEpisodeToAir is not None
                else None
            ),
        )


@strawberry.type
class EdgeMediaNetwork:
    id: int = strawberry.field(description="Unique ID for the network")
    isPrimary: bool = strawberry.field(
        description="Indicates if this is the primary network"
    )
    name: str = strawberry.field(description="Name of the network")
    originCountry: str = strawberry.field(description="Origin country of the network")
    category: NetworkCategoryEnum = strawberry.field(
        description="Category of the network (e.g., DISTRIBUTION, PRODUCTION)"
    )
    logoPath: Optional[str] = strawberry.field(
        description="Path or URL to the network's logo", default=None
    )

    @classmethod
    def from_model(cls, model: SeriesNetwork) -> "EdgeMediaNetwork":
        return cls(
            id=model.id,
            isPrimary=model.isPrimary,
            name=model.name,
            originCountry=model.originCountry,
            category=NetworkCategoryEnum(model.category),
            logoPath=model.logoPath,
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

    @classmethod
    def from_model(cls, model: SeriesTrailer) -> "EdgeMediaTrailer":
        return cls(id=model.id, site=model.site, thumbnail=model.thumbnail)


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

    @classmethod
    def from_model(cls, model: SeriesCoverImage) -> "EdgeCoverImage":
        return cls(
            extraLarge=model.extraLarge,
            large=model.large,
            medium=model.medium,
            color=model.color,
        )


@strawberry.type
class EdgeMediaTheme:
    id: str = strawberry.field(description="Unique ID for the anime theme song")
    name: str = strawberry.field(description="Name or title of the theme song")
    video: str = strawberry.field(description="URL to the video of the theme song")
    meta: "EdgeMediaThemeMeta" = strawberry.field(
        description="Metadata about the theme song, including type, number, and version."
    )
    audio: Optional[str] = strawberry.field(
        description="URL to the audio track of the theme song", default=None
    )

    @classmethod
    def from_model(cls, model: AnimeTheme) -> "EdgeMediaTheme":
        return cls(
            id=model.id,
            name=model.name,
            video=model.video,
            meta=EdgeMediaThemeMeta.from_model(model.meta),
            audio=model.audio,
        )


@strawberry.type
class EdgeMediaThemeMeta:
    type: ThemeSongTypeEnum = strawberry.field(
        description="Type of the theme song (e.g., OP for opening, ED for ending)"
    )
    number: int = strawberry.field(
        description="Sequence number of the theme (e.g., 1 for OP1, 2 for OP2)"
    )
    version: int = strawberry.field(
        description="Version number of the theme (e.g., for themes with multiple visual versions)"
    )

    @classmethod
    def from_model(cls, model: AnimeThemeMeta) -> "EdgeMediaThemeMeta":
        return cls(
            type=ThemeSongTypeEnum(model.type),
            number=model.number,
            version=model.version,
        )


@strawberry.type
class MediaType:
    id: str = strawberry.field(
        description="The unique identifier for the media entity (often corresponds to the Notify.moe edge ID)."
    )
    kind: MediaKindEnum = strawberry.field(
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
    classification: Optional[str] = strawberry.field(
        description="Content classification where available.", default=None
    )
    duration: Optional[int] = strawberry.field(
        description="Episode or chapter duration in minutes, when provided.", default=None
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

    @classmethod
    def from_entity(cls, entity: MediaEntity) -> "MediaType":
        images: List[EdgeImage] = [
            EdgeImage(
                height=image.height,
                width=image.width,
                url=image.url,
                type=image.type,
                locale=image.locale,
            )
            for image in entity.images
        ]

        theme_songs = [EdgeMediaTheme.from_model(theme) for theme in entity.themeSongs]
        trailers = [EdgeMediaTrailer.from_model(trailer) for trailer in entity.trailers]
        networks = [EdgeMediaNetwork.from_model(network) for network in entity.networks]

        return cls(
            id=entity.id,
            kind=MediaKindEnum(entity.kind),
            mediaId=EdgeMediaId.from_model(entity.mediaId),
            cover=EdgeCoverImage.from_model(entity.cover),
            title=EdgeMediaTitle.from_model(entity.title),
            updatedAt=Instant(entity.updatedAt),
            images=images,
            banner=entity.banner,
            fanart=entity.fanart,
            format=entity.format,
            status=entity.status,
            source=entity.source,
            ageRating=entity.ageRating,
            description=entity.description,
            moreInfo=entity.moreInfo,
            classification=entity.classification,
            duration=entity.duration,
            themeSongs=theme_songs,
            schedule=(
                EdgeAiringSchedule.from_model(entity.schedule)
                if entity.schedule is not None
                else None
            ),
            trailers=trailers,
            networks=networks,
            airedEpisodes=entity.airedEpisodes,
            broadcast=entity.broadcast,
            isAdult=entity.isAdult,
            homepage=entity.homepage,
            chapters=entity.chapters,
            volumes=entity.volumes,
            publishedFrom=(
                Instant(entity.publishedFrom)
                if entity.publishedFrom is not None
                else None
            ),
            publishedTo=(
                Instant(entity.publishedTo) if entity.publishedTo is not None else None
            ),
        )

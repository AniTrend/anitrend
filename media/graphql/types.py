import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from media.models import Media, Source, Airing, Season, MetaData, Information, Episode, Image
from ..di import MediaRepositoryContainer as Container
from .enums import StatusType, MediaType, SeasonType


class SourceObjectType(DjangoObjectType):
    anidb = graphene.Int(description="Identifier for anidb")
    anilist = graphene.Int(description="Identifier for anilist")
    animeplanet = graphene.String(description="Identifier for animeplanet")
    kitsu = graphene.Int(description="Identifier for kitsu")
    mal = graphene.Int(description="Identifier for mal")
    notify = graphene.String(description="Identifier for notify")
    trakt = graphene.Int(description="Identifier for trakt")
    tvdb = graphene.Int(description="Identifier for tvdb")
    crunchy = graphene.String(description="Identifier for crunchyroll")

    class Meta:
        name = "Source"
        description = "Other source ids of where this media can be found"
        model = Source
        exclude = ["id", "media"]


class AiringObjectType(DjangoObjectType):
    airing_status = StatusType(
        name="status",
        description="Url of the related item of this media"
    )
    airing_season = SeasonType(
        name="season",
        description="Season the media was aired",
        required=True,
    )
    airing_year = graphene.Int(
        name="year",
        description="Year the media was aired"
    )

    class Meta:
        name = "Airing"
        description = "Airing information about the media"
        model = Airing
        exclude = ["id", "media"]


class ImageObjectType(DjangoObjectType):
    poster = graphene.String(
        name="poster",
        description="Highest quality of poster image"
    )
    banner_extra_large = graphene.String(
        name="bannerExtraLarge",
        description="Highest quality of banner image"
    )
    banner_large = graphene.String(
        name="bannerLarge",
        description="Standard quality of banner image"
    )

    class Meta:
        name = "Image"
        description = "Images for media items"
        model = Image
        exclude = ["id", "media", "season", "episode"]


class InformationObjectType(DjangoObjectType):
    description = graphene.String(name="synopsis", description="Synopsis for the media")
    slug = graphene.String(description="Slug for the media, typically anime-planet or crunchyroll")
    alternative_titles = graphene.List(
        graphene.String,
        name="alternativeTitles",
        description="Other titles",
        required=True)
    maturity_ratings = graphene.List(
        graphene.String,
        name="maturityRatings",
        description="Age ratings",
        required=True)

    class Meta:
        name = "Information"
        description = "Additional information for the media"
        model = Information
        exclude = ["id", "media"]


class MetaDataObjectType(DjangoObjectType):
    season_number = graphene.Int(
        name="seasonNumber",
        description="The season number of this media entry"
    )
    episode_count = graphene.Int(
        name="episodeCount",
        description="The number of episodes for this season"
    )
    content_provider = graphene.String(
        name="contentProvider",
        description="Platform / Studio that produced this media"
    )
    is_mature = graphene.Boolean(
        name="isMature",
        description="If this media is considered to be for an adult audience"
    )

    class Meta:
        name = "Attribute"
        description = "Other non-standard information for the media"
        model = MetaData
        exclude = ["id", "media"]


class MediaObjectType(DjangoObjectType):
    title = graphene.String(
        description="Title of the media",
        required=True,
    )
    information = graphene.Field(
        InformationObjectType,
        description="Additional information for the media",
        required=True
    )
    airing = graphene.Field(
        AiringObjectType,
        description="Airing information for the media",
        required=True
    )
    image = graphene.Field(
        ImageObjectType,
        description="Images available for the media",
        required=True
    )
    source = graphene.Field(
        SourceObjectType,
        description="Other sources",
        required=True,
    )
    meta_data = graphene.Field(
        MetaDataObjectType,
        name="attribute",
        description="",
        required=True
    )
    type = MediaType(
        description="Media type",
        required=True,
    )
    related = graphene.List(
        graphene.String,
        required=True,
        description="Related media urls"
    )
    tags = graphene.List(
        graphene.String,
        required=True,
        description="Tags"
    )
    updated_at = graphene.DateTime(
        name="updatedAt",
        description="Last updated time",
        required=True,
    )

    class Meta:
        name = "Media"
        description = "A representation of a media item"
        model = Media
        exclude = ["season"]


class EpisodeObjectType(DjangoObjectType):
    episode_id = graphene.ID(
        name="id",
        description="The ID of the object",
        required=True,
    )
    episode = graphene.String(
        description="Episode represented in string format",
        required=True,
    )
    episode_number = graphene.Int(
        name="episodeNumber",
        description="Numerical episode number",
        required=True,
    )
    sequence_number = graphene.Float(
        name="sequenceNumber",
        description="Natural order position for the episode",
        required=True,
    )
    production_episode_id = graphene.String(
        name="productionId",
        description="Production id for the episode",
        required=True,
    )
    title = graphene.String(
        description="Title for the episode",
        required=True,
    )
    description = graphene.String(
        name="synopsis",
        description="Synopsis for the episode",
        required=True,
    )
    is_mature = graphene.String(
        name="isMature",
        description="Indicates if the episode is for a mature audience",
        required=True,
    )
    episode_air_date = graphene.DateTime(
        name="airedAt",
        description="Time and date the episode was aired",
        required=True,
    )
    media_type = graphene.String(
        name="mediaType",
        description="Media type for teh episode",
        required=True,
    )
    slug = graphene.String(
        description="Episode specific slug",
        required=True,
    )
    image = graphene.Field(
        ImageObjectType,
        description="Images for the episode",
        required=True
    )
    duration_ms = graphene.Int(
        name="duration",
        description="Duration in milliseconds of the episode",
        required=True,
    )
    listing_id = graphene.String(
        name="listingId",
        description="",
        required=True,
    )
    subtitle_locales = graphene.List(
        graphene.String,
        name="subtitleLocales",
        description="A list of subtitle locales available for the episode",
        required=True,
    )

    class Meta:
        name = "Episode"
        description = "An episode for a media"
        model = Episode
        exclude = ["season"]


class MediaSeasonObjectType(DjangoObjectType):
    media = graphene.Field(
        MediaObjectType,
        description="The parent media item for represented by this season",
        required=True,
    )
    season_id = graphene.ID(
        name="id",
        description="The ID of the object",
        required=True,
    )
    title = graphene.String(
        description="Title of the season",
        required=True,
    )
    season_number = graphene.String(
        name="seasonNumber",
        description="Season number",
        required=True,
    )
    description = graphene.String(
        name="synopsis",
        description="Synopsis for the season",
        required=True,
    )
    image = graphene.Field(
        ImageObjectType,
        description="Images for the season",
        required=True
    )
    episodes = graphene.Field(
        EpisodeObjectType,
        name="episodes",
        description="List of episodes for this season",
        required=True,
    )

    class Meta:
        name = "Season"
        description = "A representation tv season style for a media item"
        model = Season

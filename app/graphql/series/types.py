import graphene
from graphene_django import DjangoObjectType

from ...modules.series.models import Series, Source, Airing, Season, MetaData, Information, Episode, Image
from ...modules.series.di import SeriesRepositoryContainer as Container
from .enums import StatusType, SeriesType, SeasonType
from .nodes import SeriesNode, SeasonNode


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
        description = "Other source ids of where this series can be found"
        model = Source
        exclude = ["id", "series"]


class AiringObjectType(DjangoObjectType):
    airing_status = StatusType(
        name="status",
        description="Url of the related item of this series"
    )
    airing_season = SeasonType(
        name="season",
        description="Season the series was aired",
        required=True,
    )
    airing_year = graphene.Int(
        name="year",
        description="Year the series was aired"
    )

    class Meta:
        name = "Airing"
        description = "Airing information about the series"
        model = Airing
        exclude = ["id", "series"]


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
        exclude = ["id", "series", "season", "episode"]


class InformationObjectType(DjangoObjectType):
    description = graphene.String(name="synopsis", description="Synopsis for the series")
    slug = graphene.String(description="Slug for the series, typically anime-planet or crunchyroll")
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
        description = "Additional information for the series"
        model = Information
        exclude = ["id", "series"]


class MetaDataObjectType(DjangoObjectType):
    season_number = graphene.Int(
        name="seasonNumber",
        description="The season number of this series entry"
    )
    episode_count = graphene.Int(
        name="episodeCount",
        description="The number of episodes for this season"
    )
    content_provider = graphene.String(
        name="contentProvider",
        description="Platform / Studio that produced this series"
    )
    is_mature = graphene.Boolean(
        name="isMature",
        description="If this series is considered to be for an adult audience"
    )

    class Meta:
        name = "Attribute"
        description = "Other non-standard information for the series"
        model = MetaData
        exclude = ["id", "series"]


class SeriesObjectType(DjangoObjectType):
    title = graphene.String(
        description="Title of the series",
        required=True,
    )
    information = graphene.Field(
        InformationObjectType,
        description="Additional information for the series",
        required=True
    )
    airing = graphene.Field(
        AiringObjectType,
        description="Airing information for the series",
        required=True
    )
    image = graphene.Field(
        ImageObjectType,
        description="Images available for the series",
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
    type = SeriesType(
        description="Series type",
        required=True,
    )
    related = graphene.List(
        graphene.String,
        required=True,
        description="Related series urls"
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
        name = "Series"
        description = "A representation of a series item"
        model = Series
        interfaces = (SeriesNode,)
        exclude = ["season"]

    @classmethod
    def get_node_from_param(cls, info, param, repository=Container.series_repository()):
        try:
            entity = repository.get_by_param(param)
            return entity
        except cls._meta.model.DoesNotExist:
            return None


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
        description = "An episode for a series"
        model = Episode
        exclude = ["season"]


class SeasonObjectType(DjangoObjectType):
    series = graphene.Field(
        SeriesObjectType,
        description="The parent series item for represented by this season",
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
    episodeSet = graphene.Field(
        EpisodeObjectType,
        name="episodes",
        description="List of episodes for this season",
        required=True,
    )

    class Meta:
        name = "Season"
        description = "A representation tv season style for a series item"
        model = Season
        interfaces = (SeasonNode,)
        exclude = []

    @classmethod
    def get_node_from_param(cls, info, param, repository=Container.series_repository()):
        try:
            entity = repository.get_by_season_param(param)
            return entity
        except cls._meta.model.DoesNotExist:
            return None

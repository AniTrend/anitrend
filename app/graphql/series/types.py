import graphene
from graphene_django import DjangoObjectType

from ...modules.series.models import Series, Source, Relation
from ...modules.series.di import SeriesRepositoryContainer as Container
from .enums import StatusType, SeriesType, SeasonType
from .nodes import SeriesNode


class SourceObjectType(DjangoObjectType):
    trakt = graphene.Int(description="Identifier for trakt")
    tvdb = graphene.Int(description="Identifier for tvdb")
    tmdb = graphene.Int(description="Identifier for tmdb")
    anidb = graphene.Int(description="Identifier for anidb")
    anilist = graphene.Int(description="Identifier for anilist")
    animeplanet = graphene.String(description="Identifier for animeplanet")
    kitsu = graphene.Int(description="Identifier for kitsu")
    mal = graphene.Int(description="Identifier for mal")
    notify = graphene.String(description="Identifier for notify")

    class Meta:
        name = "Source"
        description = "Other source ids of where this series can be found"
        model = Source
        exclude = ["id", "series"]


class RelationObjectType(DjangoObjectType):
    url = graphene.String(
        description="Url of the related item of this series",
        required=True,
    )

    class Meta:
        name = "Relation"
        description = "Related media urls"
        model = Relation
        exclude = ["id", "series"]


class SeriesObjectType(DjangoObjectType):
    title = graphene.String(
        description="Title of the series",
        required=True,
    )
    source = graphene.Field(
        SourceObjectType,
        description="Other sources",
        required=True,
    )
    year = graphene.Int(description="Release year")
    season = SeasonType(
        description="Release season",
        required=True,
    )
    type = SeriesType(
        description="Series type",
        required=True,
    )
    episodes = graphene.Int(
        description="Number of episodes",
        required=True,
    )
    status = StatusType(
        description="Series type",
        required=True,
    )
    picture = graphene.String(
        description="Primary picture of the series"
    )
    thumbnail = graphene.String(
        description="Primary picture of the series"
    )
    relationSet = graphene.List(
        RelationObjectType,
        required=True,
        description="Related series urls"
    )
    updated_at = graphene.Int(
        description="Last updated time",
        required=True,
    )

    class Meta:
        name = "Series"
        description = "A representation of a series item"
        model = Series
        interfaces = (SeriesNode,)

    @classmethod
    def get_node_from_param(cls, info, param, repository=Container.series_repository()):
        try:
            entity = repository.get_by_param(param)
            return entity
        except cls._meta.model.DoesNotExist:
            return None

from graphene import ObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .nodes import SeriesNode, SeasonNode
from .types import SeriesObjectType, SeasonObjectType
from .filters import SeriesPagingFilterSet


class SeriesQueries(ObjectType):
    series = SeriesNode.Field(
        SeriesObjectType,
        description="Find a series item by filtering with an id",
    )
    season = SeasonNode.Field(
        SeasonObjectType,
        description="Find a season item by filtering with a series or season id",
    )
    seriesPaged = DjangoFilterConnectionField(
        SeriesObjectType,
        filterset_class=SeriesPagingFilterSet,
        description="Discover a from a paged list of items"
    )


class SeriesMutations(ObjectType):
    pass

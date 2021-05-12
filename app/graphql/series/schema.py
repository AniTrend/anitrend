from graphene import ObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .nodes import SeriesNode
from .types import SeriesObjectType
from .filters import SeriesPagingFilterSet


class SeriesQueries(ObjectType):
    series = SeriesNode.Field(
        SeriesObjectType,
        description="Find a series item by filtering with an id",
    )
    seriesPaged = DjangoFilterConnectionField(
        SeriesObjectType,
        filterset_class=SeriesPagingFilterSet,
        description="Discover a from a paged list of items"
    )


class SeriesMutations(ObjectType):
    pass

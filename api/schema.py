import api.types
import api.nodes
from graphene import ObjectType
from graphene_django.filter import DjangoFilterConnectionField

from api.filters import SeriesPagingFilter


class Query(ObjectType):
    series = api.nodes.SeriesNode.Field(
        api.types.Series,
        description="Find specific series item"
    )
    seriesPaged = DjangoFilterConnectionField(
        api.types.Series,
        filterset_class=SeriesPagingFilter,
        description="Discover a from a paged list of items"
    )


class Mutation(ObjectType):
    pass

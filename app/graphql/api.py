import graphene
from .series.schema import SeriesQueries, SeriesMutations


class Query(SeriesQueries, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(SeriesMutations, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


# noinspection PyTypeChecker
schema = graphene.Schema(
    query=Query,
    # mutation=Mutation
)

import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from config.graphql.queries import ConfigQuery
from news.graphql.queries import NewsQuery


@strawberry.type
class Mutation:
    pass


@strawberry.type
class Query(ConfigQuery, NewsQuery):
    pass


schema = strawberry.Schema(
    query=Query,
    # mutation=Mutations,
    # types=[],
    extensions=[DjangoOptimizerExtension],
)

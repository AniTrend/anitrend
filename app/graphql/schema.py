import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from config.graphql.queries import ConfigQuery
from news.graphql.queries import NewsQuery
from media.graphql.queries import MediaQuery


@strawberry.type
class Mutation:
    pass


@strawberry.type
class Query(ConfigQuery, NewsQuery, MediaQuery):
    pass


schema = strawberry.Schema(
    query=Query,
    # mutation=Mutations,
    # types=[],
    extensions=[DjangoOptimizerExtension],
)

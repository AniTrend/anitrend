import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from config.graphql.queries import ConfigQuery


@strawberry.type
class Mutations:
    pass


@strawberry.type
class Query(ConfigQuery):
    pass


schema = strawberry.Schema(
    query=Query,
    #mutation=Mutations,
    types=[],
    extensions=[DjangoOptimizerExtension],
)

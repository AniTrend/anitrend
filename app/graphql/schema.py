import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from config.graphql.queries import ConfigQuery
from news.graphql.queries import NewsQuery
from media.graphql.queries import MediaQuery
from episode.graphql.queries import EpisodeQuery


@strawberry.type
class Mutation:
    pass


@strawberry.type
class Query(ConfigQuery, NewsQuery, MediaQuery, EpisodeQuery):
    pass


from core.graphql.types import Instant, InstantScalar

schema = strawberry.Schema(
    query=Query,
    # mutation=Mutations,
    # types=[],
    extensions=[DjangoOptimizerExtension],
    scalar_overrides={
        Instant: InstantScalar,
    },
)

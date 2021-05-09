import graphene
import api.schema


class Query(api.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(api.schema.Mutation, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


# noinspection PyTypeChecker
schema = graphene.Schema(
    query=Query,
    # mutation=Mutation
)

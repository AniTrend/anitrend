import graphene

from .types import NavigationObjectType


class NavigationQuery(graphene.ObjectType):
    navigation = graphene.List(
        NavigationObjectType,
    )

    @staticmethod
    def resolve_navigation(root, info, **kwargs):
        pass

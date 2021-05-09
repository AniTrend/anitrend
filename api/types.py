from .dependencies import RepositoryProvider

import api.models
import api.nodes
import graphene
from graphene_django import DjangoObjectType


class Series(DjangoObjectType):
    __repository = RepositoryProvider.series_repository()

    class Meta:
        description = "Single series model"
        model = api.models.Series
        interfaces = (api.nodes.SeriesNode,)

    @classmethod
    def get_node_from_param(cls, info, param):
        try:
            entity = cls.__repository.get_by_param(param)
            return entity
        except cls._meta.model.DoesNotExist:
            return None


class Synonym(DjangoObjectType):
    name = graphene.String(description="Alternative name for the series")

    class Meta:
        description = "Alternative name model for a series"
        model = api.models.Synonym
        exclude = ["id"]


class Source(DjangoObjectType):
    class Meta:
        description = "Alternative source ids"
        model = api.models.Source
        exclude = ["id"]


class Relation(DjangoObjectType):
    class Meta:
        description = "Related media urls"
        model = api.models.Relation
        exclude = ["id"]


class Tag(DjangoObjectType):
    class Meta:
        description = "Tags for a series"
        model = api.models.Tag
        exclude = ["id"]

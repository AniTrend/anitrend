from typing import Optional

from graphene.relay import Node

from app import AppContainer
from .fields import SeriesNodeField, SeasonNodeField
from ...modules.series.data import SeriesParams, SeasonParams


class SeriesNode(Node):
    """Series node with ID"""
    __logging_utility = AppContainer.logging_utility().get_default_logger(__name__)

    @classmethod
    def Field(cls, *args, **kwargs):
        return SeriesNodeField(cls, *args, **kwargs)

    @classmethod
    def node_resolver(cls, only_type, root, info, **kwargs):
        if kwargs.get("id") is not None:
            return cls.get_node_from_global_id(info, kwargs.pop("id"), only_type=only_type)
        params = SeriesParams(
            tvdb=kwargs.pop("tvdb", None),
            anidb=kwargs.pop("anidb", None),
            anilist=kwargs.pop("anilist", None),
            animeplanet=kwargs.pop("animeplanet", None),
            notify=kwargs.pop("notify", None),
            kitsu=kwargs.pop("kitsu", None),
            mal=kwargs.pop("mal", None),
        )
        return cls.get_node_from_param(info, params, only_type=only_type)

    @classmethod
    def get_node_from_param(cls, info, param, only_type=None):
        try:
            graphene_type = info.schema.get_type("Series").graphene_type
        except Exception as e:
            cls.__logging_utility.warning("Failed to resolve type", exc_info=e)
            return None

        if only_type:
            # noinspection PyProtectedMember
            assert graphene_type == only_type, f"Must receive a {only_type._meta.name} id."

        get_node_from_param = getattr(graphene_type, "get_node_from_param", None)
        if get_node_from_param:
            return get_node_from_param(info, param)


class SeasonNode(Node):
    """Series node with ID"""
    __logging_utility = AppContainer.logging_utility().get_default_logger(__name__)

    @classmethod
    def Field(cls, *args, **kwargs):
        return SeasonNodeField(cls, *args, **kwargs)

    @classmethod
    def node_resolver(cls, only_type, root, info, **kwargs):
        if kwargs.get("id") is not None:
            return cls.get_node_from_global_id(info, kwargs.pop("id"), only_type=only_type)
        series_id = kwargs.pop("seriesId", None)
        return cls.get_node_from_param(info, series_id, only_type=only_type)

    @classmethod
    def get_node_from_param(cls, info, series_id: Optional[str], only_type=None):
        try:
            graphene_type = info.schema.get_type("Season").graphene_type
            _type, _id = cls.from_global_id(series_id)
        except Exception as e:
            cls.__logging_utility.warning("Failed to resolve type", exc_info=e)
            return None

        if only_type:
            # noinspection PyProtectedMember
            assert graphene_type == only_type, f"Must receive a {only_type._meta.name} id."

        get_node_from_param = getattr(graphene_type, "get_node_from_param", None)
        if get_node_from_param:
            return get_node_from_param(info, SeasonParams(seriesId=_id))

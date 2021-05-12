from graphene import ID, Int, String
from graphene.relay import Node
from graphene.relay.node import NodeField

from app import AppContainer
from ...modules.series.data import SeriesParams


class SeriesNodeField(NodeField):

    # noinspection PyShadowingBuiltins
    def __init__(self, node, type=False, description=None, **kwargs):
        assert issubclass(node, Node), "NodeField can only operate in Nodes"
        self.node_type = node
        self.field_type = type
        super(NodeField, self).__init__(
            type or node,
            description=description,
            id=ID(required=False, description="Series Id"),
            tvdb=Int(required=False, description="TVDB Id"),
            anidb=Int(required=False, description="AniDB Id"),
            anilist=Int(required=False, description="AniList Id"),
            animeplanet=String(required=False, description="AnimePlanet Slug"),
            notify=String(required=False, description="Notify.moe Id"),
            kitsu=Int(required=False, description="Kitsu Id"),
            mal=Int(required=False, description="Mal Id"),
            **kwargs
        )


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

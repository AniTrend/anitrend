from graphene import ID, Int, String
from graphene.relay import Node
from graphene.relay.node import NodeField


class MediaNodeField(NodeField):

    # noinspection PyShadowingBuiltins
    def __init__(self, node, type=False, description=None, **kwargs):
        assert issubclass(node, Node), "NodeField can only operate in Nodes"
        self.node_type = node
        self.field_type = type
        super(NodeField, self).__init__(
            type or node,
            description=description,
            id=ID(required=False, description="Media Id"),
            tvdb=Int(required=False, description="TVDB Id"),
            anidb=Int(required=False, description="AniDB Id"),
            anilist=Int(required=False, description="AniList Id"),
            animeplanet=String(required=False, description="AnimePlanet Slug"),
            notify=String(required=False, description="Notify.moe Id"),
            kitsu=Int(required=False, description="Kitsu Id"),
            mal=Int(required=False, description="Mal Id"),
            **kwargs
        )


class SeasonNodeField(NodeField):

    # noinspection PyShadowingBuiltins
    def __init__(self, node, type=False, description=None, **kwargs):
        assert issubclass(node, Node), "NodeField can only operate in Nodes"
        self.node_type = node
        self.field_type = type
        super(NodeField, self).__init__(
            type or node,
            description=description,
            id=ID(required=False, description="Season Id"),
            mediaId=ID(required=False, description="Media Id"),
            **kwargs
        )

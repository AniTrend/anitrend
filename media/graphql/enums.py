import graphene

from core import str_to_enum
from .. import MediaTypes, StatusTypes, SeasonTypes

MediaType = graphene.Enum(
    "MediaType",
    [(str_to_enum(choice[0]), choice[0]) for choice in MediaTypes.CHOICES]
)

StatusType = graphene.Enum(
    "StatusType",
    [(str_to_enum(choice[0]), choice[0]) for choice in StatusTypes.CHOICES],
)

SeasonType = graphene.Enum(
    "SeasonType",
    [(str_to_enum(choice[0]), choice[0]) for choice in SeasonTypes.CHOICES]
)

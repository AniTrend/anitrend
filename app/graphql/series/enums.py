import graphene

from ..utilities import str_to_enum
from ...modules.series import SeasonTypes, SeriesTypes, StatusTypes

SeriesType = graphene.Enum(
    "SeriesType",
    [(str_to_enum(choice[0]), choice[0]) for choice in SeriesTypes.CHOICES]
)

StatusType = graphene.Enum(
    "StatusType",
    [(str_to_enum(choice[0]), choice[0]) for choice in StatusTypes.CHOICES]
)

SeasonType = graphene.Enum(
    "SeasonType",
    [(str_to_enum(choice[0]), choice[0]) for choice in SeasonTypes.CHOICES]
)


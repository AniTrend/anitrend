import graphene
from graphene_django import DjangoObjectType

from ..models import Group, Navigation, Destination


class GroupObjectType(DjangoObjectType):
    identifier = graphene.Int(
        name="identifier",
        description="Group ID"
    )
    authenticated = graphene.Boolean(
        name="authenticated",
        description="Authenticated status"
    )
    i18n = graphene.String(
        name="i18n",
        description="Group internationalization"
    )

    class Meta:
        name = "Group"
        description = "Navigation group properties"
        model = Group


class DestinationObjectType(DjangoObjectType):
    destination = graphene.String(
        name="destination",
        description="Navigation destination"
    )
    type = graphene.String(
        name="type",
        description="Navigation destination",
    )

    class Meta:
        name = "Destination"
        description = "Navigation destination properties"
        model = Destination
        convert_choices_to_enum = True


class NavigationObjectType(DjangoObjectType):
    i18n = graphene.String(
        name="i18n",
        description="Navigation internationalization"
    )
    icon = graphene.String(
        name="icon",
        description="Navigation icon"
    )
    destination = graphene.Field(DestinationObjectType)
    group = graphene.Field(GroupObjectType)

    class Meta:
        name = "Navigation"
        description = "Navigation configuration"
        model = Navigation
        exclude = []

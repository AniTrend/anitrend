import graphene
from graphene_django import DjangoObjectType


class ImageResourceObjectType(DjangoObjectType):
    banner = graphene.String(
        name="banner",
        description="Banner image URL"
    )
    poster = graphene.String(
        name="poster",
        description="Poster image URL"
    )
    loading = graphene.String(
        name="loading",
        description="Loading image URL"
    )
    error = graphene.String(
        name="error",
        description="Error image URL"
    )
    info = graphene.String(
        name="info",
        description="Info image URL"
    )
    default = graphene.String(
        name="default",
        description="Default image URL"
    )

    class Meta:
        name = "ImageResource"
        description = "Image resource properties"
        exclude = ["id"]


class GroupObjectType(DjangoObjectType):
    id = graphene.Int(
        name="id",
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
        exclude = ["id"]


class NavigationObjectType(DjangoObjectType):
    id = graphene.Int(
        name="id",
        description="Navigation ID"
    )
    destination = graphene.String(
        name="destination",
        description="Navigation destination"
    )
    i18n = graphene.String(
        name="i18n",
        description="Navigation internationalization"
    )
    icon = graphene.String(
        name="icon",
        description="Navigation icon"
    )
    group = GroupObjectType()

    class Meta:
        name = "Navigation"
        description = "Navigation items for clients"
        exclude = ["id"]


class SettingsObjectType(DjangoObjectType):
    analytics_enabled = graphene.Boolean(
        name="analyticsEnabled",
        description="Analytics enabled status"
    )

    class Meta:
        name = "Settings"
        description = "Client configuration properties"
        exclude = ["id"]


class GenreMappingObjectType(DjangoObjectType):
    genre = graphene.String(
        name="genre",
        description="Genre"
    )
    mediaId = graphene.Int(
        name="mediaId",
        description="Media ID"
    )

    class Meta:
        name = "GenreMapping"
        description = "Genre and media ID relation"
        exclude = ["id"]


class ConfigurationObjectType(DjangoObjectType):
    settings = SettingsObjectType()
    image = ImageResourceObjectType()
    navigation = graphene.List(NavigationObjectType)
    genreMappings = graphene.List(GenreMappingObjectType)

    class Meta:
        name = "Configuration"
        description = "Client configuration properties"
        exclude = ["id"]

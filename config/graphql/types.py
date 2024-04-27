import graphene
from graphene import ObjectType


class NavigationGroupObjectType(ObjectType):
    authenticated = graphene.Boolean(
        name="authenticated",
        description="Should only display when viewer is authenticated"
    )
    i18n = graphene.String(
        name="i18n",
        description="Language resource associated with grouping"
    )

    class Meta:
        name = "NavigationGroup"
        description = "Category for a navigation item"


class NavigationObjectType(ObjectType):
    criteria = graphene.String(
        name="criteria",
        description="Display criteria as semver"
    )
    destination = graphene.String(
        name="destination",
        description="Target destination"
    )
    i18n = graphene.String(
        name="i18n",
        description="Language resource associated with grouping"
    )
    icon = graphene.String(
        name="icon",
        description="Image resource associated with the navigation item"
    )
    group = graphene.Field(
        NavigationGroupObjectType,
        name="group",
        description="Associated group for this navigation item"
    )

    class Meta:
        name = "Navigation"
        description = "Navigation configuration for an entry"


class GenreObjectType(ObjectType):
    name = graphene.String(
        name="name",
        description="Genre title"
    )
    mediaId = graphene.Int(
        name="mediaId",
        description="Related media ID"
    )

    class Meta:
        name = "Genre"
        description = "Genre and media ID relation"


class DefaultImageObjectType(ObjectType):
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


class SettingsObjectType(ObjectType):
    analyticsEnabled = graphene.Boolean(
        name="analyticsEnabled",
        description="Analytics enabled status"
    )
    platformSource = graphene.String(
        name="platformSource",
        description="Upstream platform for additional services"
    )

    class Meta:
        name = "Settings"
        description = "Client default settings"


class ConfigurationObjectType(ObjectType):
    settings = graphene.Field(
        SettingsObjectType,
        name="settings",
        description="Configuration settings"
    )
    image = graphene.Field(
        DefaultImageObjectType,
        name="image",
        description="Default image resources"
    )
    navigation = graphene.List(
        NavigationObjectType,
        name="navigation",
        description="Navigation configurations"
    )
    genres = graphene.List(
        GenreObjectType,
        name="genres",
        description="Genre and media connections"
    )

    class Meta:
        name = "Configuration"
        description = "Client configuration"

import graphene
from graphene_django import DjangoObjectType

from ..models import Settings, DefaultImage, Config


class DefaultImageObjectType(DjangoObjectType):
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
        model = DefaultImage


class SettingsObjectType(DjangoObjectType):
    analytics_enabled = graphene.Boolean(
        name="analyticsEnabled",
        description="Analytics enabled status"
    )

    class Meta:
        name = "Settings"
        description = "Client default settings"
        model = Settings


class ConfigurationObjectType(DjangoObjectType):
    settings = graphene.Field(
        SettingsObjectType,
        name="settings",
        description="Configuration settings"
    )
    default_image = graphene.Field(
        DefaultImageObjectType,
        name="defaultImage",
        description="Default image resources"
    )

    class Meta:
        name = "Configuration"
        description = "Client configuration"
        model = Config

import strawberry
from typing import Optional, List
from strawberry.types import Info

from .resolvers import resolve_config

@strawberry.type
class ImageResource:
    banner: Optional[str] = strawberry.field(description="Banner image URL")
    default: Optional[str] = strawberry.field(description="Default image URL")
    error: Optional[str] = strawberry.field(description="Error image URL")
    info: Optional[str] = strawberry.field(description="Info image URL")
    loading: Optional[str] = strawberry.field(description="Loading image URL")
    poster: Optional[str] = strawberry.field(description="Poster image URL")

@strawberry.type
class Settings:
    analytics_enabled: bool = strawberry.field(
        name="analyticsEnabled",
        description="Analytics enabled status"
    )
    platform_source: str = strawberry.field(
        name="platformSource",
        description="Upstream platform for additional services"
    )

@strawberry.type
class Configuration:
    settings: Settings = strawberry.field(description="Configuration settings")
    image: ImageResource = strawberry.field(description="Default image resources")

@strawberry.type
class ConfigQuery:
    @strawberry.field(description="Client configuration")
    def config(self, info: Info) -> Optional[Configuration]:
        return resolve_config(info)

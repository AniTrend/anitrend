import strawberry
from typing import Optional, List

@strawberry.type
class NavigationGroup:
    authenticated: bool = strawberry.field(
        description="Should only display when viewer is authenticated"
    )
    i18n: str = strawberry.field(
        description="Language resource associated with grouping"
    )

@strawberry.type
class Navigation:
    criteria: str = strawberry.field(
        description="Display criteria as semver"
    )
    destination: str = strawberry.field(
        description="Target destination"
    )
    i18n: str = strawberry.field(
        description="Language resource associated with grouping"
    )
    icon: str = strawberry.field(
        description="Image resource associated with the navigation item"
    )
    group: NavigationGroup = strawberry.field(
        description="Associated group for this navigation item"
    )

@strawberry.type
class Genre:
    name: str = strawberry.field(
        description="Genre title"
    )
    media_id: int = strawberry.field(
        name="mediaId",
        description="Related media ID"
    )

@strawberry.type
class ImageResource:
    banner: Optional[str] = strawberry.field(description="Banner image URL")
    poster: Optional[str] = strawberry.field(description="Poster image URL")
    loading: Optional[str] = strawberry.field(description="Loading image URL")
    error: Optional[str] = strawberry.field(description="Error image URL")
    info: Optional[str] = strawberry.field(description="Info image URL")
    default: Optional[str] = strawberry.field(description="Default image URL")

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
    settings: Settings = strawberry.field(
        description="Configuration settings"
    )
    image: ImageResource = strawberry.field(
        description="Default image resources"
    )
    navigation: List[Navigation] = strawberry.field(
        description="Navigation configurations"
    )
    genres: List[Genre] = strawberry.field(
        description="Genre and media connections"
    )

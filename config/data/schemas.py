from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class SettingsSchema:
    analyticsEnabled: bool
    platformSource: Optional[str]


@dataclass
class ImageSchema:
    banner: str
    poster: str
    loading: str
    error: str
    info: str
    default: str


@dataclass
class NavigationGroupSchema:
    authenticated: bool
    i18n: str


@dataclass
class NavigationSchema:
    criteria: str
    destination: str
    i18n: str
    icon: str
    group: NavigationGroupSchema


@dataclass
class GenreSchema:
    name: str
    mediaId: int


@dataclass
class ConfigurationSchema:
    id: str
    settings: SettingsSchema
    image: ImageSchema
    navigation: List[NavigationSchema] = field(default_factory=list)
    genres: List[GenreSchema] = field(default_factory=list)

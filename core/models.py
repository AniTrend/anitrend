from dataclasses import dataclass, field
from typing import Optional

from django.db import models
from django.db.models import QuerySet


class CommonModel(models.Model):
    objects: QuerySet = models.Manager

    class Meta:
        abstract = True


@dataclass
class UserAgent:
    family: Optional[str] = None
    major: Optional[str] = None
    minor: Optional[str] = None
    patch: Optional[str] = None

    @property
    def version(self):
        return f'{self.major}{self.minor}{self.patch}'


@dataclass
class CPU:
    architecture: Optional[str] = None


@dataclass
class Device:
    family: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None


@dataclass
class OS:
    family: Optional[str] = None
    major: Optional[str] = None
    minor: Optional[str] = None
    patch: Optional[str] = None
    patch_minor: Optional[str] = None

    @property
    def version(self):
        return f'{self.major}{self.minor}{self.patch}${self.patch_minor}'


@dataclass
class UserAgentInfo:
    raw: str
    user_agent: UserAgent = field(default_factory=UserAgent)
    cpu: CPU = field(default_factory=CPU)
    device: Device = field(default_factory=Device)
    engine: UserAgent = field(default_factory=UserAgent)
    os: OS = field(default_factory=OS)


@dataclass
class Application:
    locale: Optional[str]
    version: Optional[str]
    source: Optional[str]
    code: Optional[str]
    label: Optional[str]
    buildType: Optional[str]


@dataclass
class ContextHeader:
    authorization: Optional[str]
    accepts: Optional[str]
    content_type: Optional[str]
    accept_encoding: Optional[str]
    application: Application
    user_agent_info: UserAgentInfo

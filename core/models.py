from dataclasses import dataclass
from typing import Optional

from django.db import models
from django.db.models import QuerySet


class CommonModel(models.Model):
    objects: QuerySet = models.Manager

    class Meta:
        abstract = True


@dataclass
class Device:
    browser: Optional[str]
    cpu: Optional[str]
    device: Optional[str]
    engine: Optional[str]
    os: Optional[str]


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
    agent: str
    contentType: Optional[str]
    acceptEncoding: Optional[str]
    language: Optional[str]
    application: Application

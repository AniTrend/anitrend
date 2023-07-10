from django.db import models

from core.models import CommonModel
from .choices import DESTINATION_TYPES


class Group(CommonModel):
    identifier = models.IntegerField(unique=True)
    authenticated = models.BooleanField(default=False),
    i18n = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.i18n}"


class Destination(CommonModel):
    destination = models.CharField(max_length=128),
    type = models.CharField(max_length=25, choices=DESTINATION_TYPES)

    def __str__(self):
        return f"{self.destination}"


class Criteria(CommonModel):
    version = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.version}"


class Navigation(CommonModel):
    id = models.IntegerField(primary_key=True)
    criteria = models.OneToOneField(
        Criteria,
        on_delete=models.CASCADE
    )
    destination = models.OneToOneField(
        Destination,
        on_delete=models.CASCADE
    )
    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE
    )
    icon = models.CharField(max_length=50)
    i18n = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.i18n}"

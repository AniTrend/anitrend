from django.db import models
from django.db.models import QuerySet


class CommonModel(models.Model):
    objects: QuerySet = models.Manager

    class Meta:
        abstract = True

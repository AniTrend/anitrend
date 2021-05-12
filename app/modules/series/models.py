from django.db import models
from django.db.models import QuerySet
from django.utils import timezone

from app.modules.common import SEASON_CHOICES, TYPE_CHOICES, STATUS_CHOICES


class CommonModel(models.Model):

    objects: QuerySet = models.Manager

    class Meta:
        abstract = True


class Source(CommonModel):
    tvdb = models.IntegerField(null=True)
    anidb = models.IntegerField(null=True)
    anilist = models.IntegerField(null=True)
    animeplanet = models.CharField(max_length=256, null=True)
    kitsu = models.IntegerField(null=True)
    mal = models.IntegerField(null=True)
    notify = models.CharField(max_length=25, null=True)


class Series(CommonModel):
    title = models.CharField(max_length=256)
    source = models.OneToOneField(Source, on_delete=models.CASCADE)
    year = models.IntegerField(null=True)
    season = models.CharField(
        max_length=8,
        choices=SEASON_CHOICES
    )
    type = models.CharField(
        max_length=12,
        choices=TYPE_CHOICES
    )
    episodes = models.IntegerField()
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES
    )
    picture = models.CharField(
        max_length=128,
    )
    thumbnail = models.CharField(
        max_length=128,
    )
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("title",)


class Relation(CommonModel):
    url = models.CharField(max_length=256)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)

    def __str__(self):
        return self.url

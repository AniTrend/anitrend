from django.db import models
from django.db.models import QuerySet
from django.utils import timezone

from app.modules.common import SEASON_CHOICES, TYPE_CHOICES, STATUS_CHOICES


class CommonModel(models.Model):
    objects: QuerySet = models.Manager

    class Meta:
        abstract = True


class AnimeSource(CommonModel):
    anidb = models.IntegerField(null=True)
    anilist = models.IntegerField(null=True)
    animeplanet = models.CharField(max_length=256, null=True)
    kitsu = models.IntegerField(null=True)
    mal = models.IntegerField(null=True)
    notify = models.CharField(max_length=25, null=True)

    def __str__(self):
        if self.anilist is not None:
            return f"anilist: {str(self.anilist)}"
        if self.anidb is not None:
            return f"anidb: {str(self.anidb)}"
        if self.animeplanet is not None:
            return f"animeplanet: {str(self.animeplanet)}"
        if self.kitsu is not None:
            return f"kitsu: {str(self.kitsu)}"
        if self.mal is not None:
            return f"mal: {str(self.mal)}"
        if self.notify is not None:
            return f"notify: {str(self.notify)}"


class Anime(CommonModel):
    title = models.CharField(max_length=256)
    source = models.OneToOneField(AnimeSource, on_delete=models.CASCADE)
    year = models.IntegerField(null=True)
    season = models.CharField(
        max_length=12,
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
        max_length=256,
    )
    thumbnail = models.CharField(
        max_length=256,
    )
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("title", "updated_at")


class AnimeRelation(CommonModel):
    url = models.CharField(max_length=256)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.url}"

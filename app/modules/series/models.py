from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

from .choices import AIRING_STATUS_CHOICES, AIRING_SEASON_CHOICES, SERIES_TYPE_CHOICES
from ..common.models import CommonModel


class Source(CommonModel):
    anidb = models.IntegerField(null=True)
    anilist = models.IntegerField(null=True)
    animeplanet = models.CharField(max_length=256, null=True)
    kitsu = models.IntegerField(null=True)
    mal = models.IntegerField(null=True)
    notify = models.CharField(max_length=25, null=True)
    trakt = models.IntegerField(null=True)
    tvdb = models.IntegerField(null=True)
    crunchy = models.CharField(max_length=25, null=True)


class Airing(CommonModel):
    airing_status = models.CharField(max_length=16, choices=AIRING_STATUS_CHOICES, null=True)
    airing_season = models.CharField(max_length=8, choices=AIRING_SEASON_CHOICES)
    airing_year = models.IntegerField(null=True)


class Image(CommonModel):
    poster = models.CharField(max_length=128)
    banner_extra_large = models.CharField(max_length=128)
    banner_large = models.CharField(max_length=128)


class Information(CommonModel):
    description = models.TextField(null=True)
    slug = models.CharField(max_length=128, null=True)
    alternative_titles = ArrayField(models.CharField(max_length=128))
    maturity_ratings = ArrayField(models.CharField(max_length=16))


class MetaData(CommonModel):
    season_number = models.IntegerField(default=0)
    episode_count = models.IntegerField(default=0)
    content_provider = models.CharField(max_length=128)
    is_mature = models.BooleanField(default=False)


class Series(CommonModel):
    title = models.CharField(max_length=256)
    information = models.OneToOneField(Information, on_delete=models.CASCADE)
    airing = models.OneToOneField(Airing, on_delete=models.CASCADE)
    image = models.OneToOneField(Image, on_delete=models.CASCADE)
    source = models.OneToOneField(Source, on_delete=models.CASCADE)
    meta_data = models.OneToOneField(MetaData, on_delete=models.CASCADE)
    type = models.CharField(max_length=12, choices=SERIES_TYPE_CHOICES)
    related = ArrayField(models.CharField(max_length=256))
    tags = ArrayField(models.CharField(max_length=128))
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("title",)


class Season(CommonModel):
    series = models.OneToOneField(Series, on_delete=models.CASCADE)
    season_id = models.CharField(max_length=25, primary_key=True)
    title = models.CharField(max_length=256)
    season_number = models.CharField(max_length=25)
    description = models.TextField()
    image = models.OneToOneField(Image, on_delete=models.CASCADE)

    def __str__(self):
        prefix = ""
        if self.season_number < 9:
            prefix = "0"
        return f"S{prefix}{self.season_number} • {self.title}"

    class Meta:
        ordering = ("title", "season_number")


class Episode(CommonModel):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    episode_id = models.CharField(max_length=25, primary_key=True)
    episode = models.CharField(max_length=25)
    episode_number = models.IntegerField(null=True)
    sequence_number = models.FloatField()
    production_episode_id = models.CharField(max_length=25)
    title = models.CharField(max_length=256)
    description = models.TextField()
    is_mature = models.BooleanField()
    episode_air_date = models.DateTimeField()
    media_type = models.CharField(max_length=25)
    slug = models.CharField(max_length=25)
    image = models.OneToOneField(Image, on_delete=models.CASCADE)
    duration_ms = models.IntegerField()
    listing_id = models.CharField(max_length=25)
    subtitle_locales = ArrayField(models.CharField(max_length=16))

    def __str__(self):
        prefix = ""
        if self.episode_number < 9:
            prefix = "0"
        return f"{self.season} - E{prefix}{self.episode} • {self.title}"

    class Meta:
        ordering = ("title", "sequence_number", "episode_number", "duration_ms")

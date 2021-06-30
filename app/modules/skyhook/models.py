from django.contrib.postgres.fields import ArrayField
from django.db import models

from ..common.models import CommonModel
from .choices import STATUS_CHOICES


class Image(CommonModel):
    banner = models.URLField(null=True)
    poster = models.URLField(null=True)
    fan_art = models.URLField(null=True)


class Show(CommonModel):
    tvdb_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256)
    overview = models.TextField(null=True)
    slug = models.CharField(max_length=256)
    first_aired = models.DateField()
    tv_maze_id = models.IntegerField(unique=True)
    added = models.DateTimeField()
    last_updated = models.DateTimeField(null=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )
    runtime = models.IntegerField()
    time_of_day = models.TimeField()
    network = models.CharField(max_length=128)
    imdb_id = models.CharField(max_length=128, unique=True)
    genres = ArrayField(
        models.CharField(max_length=128)
    )
    content_rating = models.CharField(max_length=16)
    rating = models.FloatField()
    alternative_titles = ArrayField(
        models.CharField(max_length=256)
    )
    image = models.OneToOneField(Image, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("title", "last_updated", "rating", "added")


class Season(CommonModel):
    season_number = models.IntegerField()
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    image = models.OneToOneField(Image, on_delete=models.CASCADE)

    def __str__(self):
        prefix = ""
        if self.season_number < 9:
            prefix = "0"
        return f"{self.show} • S{prefix}{self.season_number}"

    class Meta:
        ordering = ("season_number",)


class Episode(CommonModel):
    tvdb_show_id = models.IntegerField(db_index=True)
    tvdb_id = models.IntegerField(db_index=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    episode_number = models.IntegerField()
    aired_after_season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name="+",
        null=True
    )
    title = models.CharField(max_length=256)
    air_date = models.DateField()
    air_date_utc = models.DateTimeField()
    overview = models.TextField(null=True)
    writers = ArrayField(
        models.CharField(max_length=256),
        null=True
    )
    directors = ArrayField(
        models.CharField(max_length=256),
        null=True
    )
    image = models.URLField(null=True)

    def __str__(self):
        prefix = ""
        if self.episode_number < 9:
            prefix = "0"
        return f"{self.season} - E{prefix}{self.episode_number} • {self.title}"

    class Meta:
        ordering = ("episode_number", "title")

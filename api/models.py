from django.db import models
from django.utils import timezone

STATUS_CHOICES = (
    ("FINISHED", "FINISHED"),
    ("CURRENTLY", "CURRENTLY"),
    ("UPCOMING", "UPCOMING"),
    ("UNKNOWN", "UNKNOWN"),
)

TYPE_CHOICES = (
    ("TV", "TV"),
    ("Movie", "Movie"),
    ("OVA", "OVA"),
    ("ONA", "ONA"),
    ("Special", "Special")
)


class CommonSourceModel(models.Model):
    tvdb = models.IntegerField(null=True)
    anidb = models.IntegerField(null=True)
    anilist = models.IntegerField(null=True)
    animeplanet = models.CharField(max_length=256, null=True)
    kitsu = models.IntegerField(null=True)
    mal = models.IntegerField(null=True)
    notify = models.CharField(max_length=25, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.anilist


class Source(CommonSourceModel):
    pass


class Relation(CommonSourceModel):
    pass


class Series(models.Model):
    title = models.CharField(max_length=256)
    source = models.OneToOneField(Source, on_delete=models.CASCADE)
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
    relation = models.OneToOneField(Relation, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("title",)


class CommonTitleModel(models.Model):
    title = models.CharField(max_length=256)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        ordering = ("title",)


class Synonym(CommonTitleModel):
    pass


class Tag(CommonTitleModel):
    pass

from django.db import models
from django.utils import timezone


class Mapping(models.Model):
    id = models.IntegerField(primary_key=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)


class MappingTitle(models.Model):
    title = models.CharField(max_length=256)
    mapping = models.ForeignKey(Mapping, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("title",)

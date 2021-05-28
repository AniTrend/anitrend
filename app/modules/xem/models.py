from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from ..common.models import CommonModel


class Xem(CommonModel):
    id = models.IntegerField(primary_key=True)
    titles = ArrayField(models.CharField(max_length=256))
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id} - {self.titles}"

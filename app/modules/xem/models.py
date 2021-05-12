from django.db import models
from django.db.models import QuerySet
from django.utils import timezone


class CommonModel(models.Model):

    objects: QuerySet = models.Manager

    class Meta:
        abstract = True


class Xem(CommonModel):
    id = models.IntegerField(primary_key=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)


class XemTitle(CommonModel):
    title = models.CharField(max_length=256)
    xem = models.ForeignKey(Xem, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.xem}"

    class Meta:
        ordering = ("title",)

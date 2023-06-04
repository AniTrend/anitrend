from django.db import models

from core.models import CommonModel


class DefaultImage(CommonModel):
    banner = models.URLField(null=True)
    poster = models.URLField(null=True)
    loading = models.URLField(null=True)
    error = models.URLField(null=True)
    info = models.URLField(null=True)
    default = models.URLField(null=True)

    def __str__(self):
        return f"banner: {self.banner}"


class Settings(CommonModel):
    analytics_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"analytics_enabled: {self.analytics_enabled}"


class Config(CommonModel):
    id = models.IntegerField(primary_key=True, auto_created=True)
    default_image = models.OneToOneField(DefaultImage, on_delete=models.CASCADE)
    settings = models.OneToOneField(Settings, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"

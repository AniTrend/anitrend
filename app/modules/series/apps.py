from django.apps import AppConfig

from app import container


class SeriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.modules.series'
    verbose_name = 'series'

    def ready(self):
        super().ready()
        container.wire(
            modules=[
                f"{self.name}.data.repositories",
            ]
        )

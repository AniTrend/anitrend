from django.apps import AppConfig

from app import container


class MediaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'media'
    verbose_name = 'media'

    def ready(self):
        super().ready()
        container.wire(
            modules=[
                f"{self.name}.data.repositories",
            ]
        )

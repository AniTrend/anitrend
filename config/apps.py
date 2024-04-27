from django.apps import AppConfig

from app import container


class Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'config'
    verbose_name = 'config'

    def ready(self):
        super().ready()
        container.wire(
            modules=[
                f"{self.name}.data.repositories",
                f"{self.name}.domain.usecases",
            ]
        )

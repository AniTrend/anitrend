from django.apps import AppConfig

from app import container


class SkyhookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.modules.skyhook'
    verbose_name = 'skyhook'

    def ready(self):
        super().ready()
        container.wire(
            modules=[
                f"{self.name}.data.repositories",
                f"{self.name}.domain.usecases",
                f"{self.name}.task.workers",
                f"{self.name}.task.hooks"
            ]
        )

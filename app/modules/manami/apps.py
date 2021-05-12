from django.apps import AppConfig

from app import container


class ManamiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.modules.manami'
    verbose_name = 'manami'

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

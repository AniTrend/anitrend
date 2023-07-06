from django.apps import AppConfig

from app import container


class ServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.modules.service'
    verbose_name = 'service'

    def ready(self):
        super().ready()
        container.wire(
            modules=[
                f"{self.name}.hooks",
                f"{self.name}.tasks"
            ]
        )

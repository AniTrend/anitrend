from django.apps import AppConfig

from app import container


class MainConfig(AppConfig):
    name = 'app.main'
    verbose_name = 'app'

    def ready(self):
        super().ready()
        container.wire(
            modules=[
                f"{self.name}.mixin",
            ]
        )

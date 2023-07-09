from django.apps import AppConfig

from app import container


class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = 'core'

    def ready(self):
        super().ready()
        container.wire(
            modules=[
                f"{self.name}.mixin",
            ]
        )

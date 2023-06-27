from ...models import Config, Settings, DefaultImage


def init_fixtures():
    settings = Settings.objects.create(
        analytics_enabled=False
    )
    default_image = DefaultImage.objects.create(
        banner="https://anitrend.co/media/banner.png",
        poster="https://anitrend.co/media/poster.png",
        loading="https://anitrend.co/media/loading.png",
        error="https://anitrend.co/media/error.png",
        info="https://anitrend.co/media/info.png",
        default="https://anitrend.co/media/default.png",
    )
    Config.objects.create(
        id=1,
        settings=settings,
        default_image=default_image
    )

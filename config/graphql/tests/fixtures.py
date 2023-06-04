from ...models import Configuration, Settings, DefaultImage


def init_fixtures():
    settings = Settings.objects.create(
        analyticsEnabled=False
    )
    default_image = DefaultImage.objects.create(
        banner="https://anitrend.co/media/banner.png",
        poster="https://anitrend.co/media/poster.png",
        loading="https://anitrend.co/media/loading.png",
        error="https://anitrend.co/media/error.png",
        info="https://anitrend.co/media/info.png",
        default="https://anitrend.co/media/default.png",
    )
    Configuration.objects.create(
        settings=settings,
        default_image=default_image
    )

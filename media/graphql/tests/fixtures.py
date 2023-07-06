from ...models import Media


def init_fixtures():
    Media.drop_collection()
    media = Media(

    )
    media.save()

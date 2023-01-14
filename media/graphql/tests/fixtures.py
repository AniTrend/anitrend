import pytest
from ...models import Media


def fixture_media_data():
    Media.drop_collection()
    media = Media(

    )
    media.save()


@pytest.fixture(scope="module")
def fixtures_data() -> bool:
    fixture_media_data()
    return True

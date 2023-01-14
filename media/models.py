from django.utils import timezone
from mongoengine import Document, IntField, StringField, ListField, BooleanField, ReferenceField, DateTimeField, \
    FloatField, CASCADE

from .choices import AIRING_STATUS_CHOICES, AIRING_SEASON_CHOICES, MEDIA_TYPE_CHOICES


class Source(Document):
    anidb = IntField(null=True)
    anilist = IntField(null=True)
    animeplanet = StringField(max_length=256, null=True)
    kitsu = IntField(null=True)
    mal = IntField(null=True)
    notify = StringField(max_length=25, null=True)
    trakt = IntField(null=True)
    tvdb = IntField(null=True)
    crunchy = StringField(max_length=25, null=True)


class Airing(Document):
    airing_status = StringField(max_length=16, choices=AIRING_STATUS_CHOICES, null=True)
    airing_season = StringField(max_length=8, choices=AIRING_SEASON_CHOICES)
    airing_year = IntField(null=True)


class Image(Document):
    poster = StringField(max_length=128)
    banner_extra_large = StringField(max_length=128)
    banner_large = StringField(max_length=128)


class Information(Document):
    description = StringField(null=True)
    slug = StringField(max_length=128, null=True)
    alternative_titles = ListField(StringField(max_length=128))
    maturity_ratings = ListField(StringField(max_length=16))


class MetaData(Document):
    season_number = IntField(default=0)
    episode_count = IntField(default=0)
    content_provider = StringField(max_length=128)
    is_mature = BooleanField(default=False)


class Media(Document):
    title = StringField(max_length=256)
    information = ReferenceField(document_type=Information, reverse_delete_rule=CASCADE)
    airing = ReferenceField(document_type=Airing, reverse_delete_rule=CASCADE)
    image = ReferenceField(document_type=Image, reverse_delete_rule=CASCADE)
    source = ReferenceField(document_type=Source, reverse_delete_rule=CASCADE)
    meta_data = ReferenceField(document_type=MetaData, reverse_delete_rule=CASCADE)
    type = StringField(max_length=12, choices=MEDIA_TYPE_CHOICES)
    related = ListField(StringField(max_length=256))
    tags = ListField(StringField(max_length=128))
    updated_at = DateTimeField(default=timezone.now().utcnow())

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("title",)


class Season(Document):
    media = ReferenceField(document_type=Media, reverse_delete_rule=CASCADE)
    season_id = StringField(max_length=25, primary_key=True)
    title = StringField(max_length=256)
    season_number = StringField(max_length=25)
    description = StringField()
    image = ReferenceField(document_type=Image, reverse_delete_rule=CASCADE)

    def __str__(self):
        prefix = ""
        if self.season_number < 9:
            prefix = "0"
        return f"S{prefix}{self.season_number} • {self.title}"

    class Meta:
        ordering = ("title", "season_number")


class Episode(Document):
    season = ReferenceField(document_type=Season, reverse_delete_rule=CASCADE)
    episode_id = StringField(max_length=25, primary_key=True)
    episode = StringField(max_length=25)
    episode_number = IntField(null=True)
    sequence_number = FloatField()
    production_episode_id = StringField(max_length=25)
    title = StringField(max_length=256)
    description = StringField()
    is_mature = BooleanField()
    episode_air_date = DateTimeField()
    media_type = StringField(max_length=25)
    slug = StringField(max_length=25)
    image = ReferenceField(document_type=Image, reverse_delete_rule=CASCADE)
    duration_ms = IntField()
    listing_id = StringField(max_length=25)
    subtitle_locales = ListField(StringField(max_length=16))

    def __str__(self):
        prefix = ""
        if self.episode_number < 9:
            prefix = "0"
        return f"{self.season} - E{prefix}{self.episode} • {self.title}"

    class Meta:
        ordering = ("title", "sequence_number", "episode_number", "duration_ms")

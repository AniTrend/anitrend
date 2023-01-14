
from django.utils import timezone
from mongoengine import Document, IntField, StringField, URLField, ListField, DateTimeField, ReferenceField, CASCADE

from .choices import SEASON_CHOICES, TYPE_CHOICES, STATUS_CHOICES


class AnimeSource(Document):
    anidb = IntField(null=True)
    anilist = IntField(null=True)
    animeplanet = StringField(max_length=256, null=True)
    kitsu = IntField(null=True)
    mal = IntField(null=True)
    notify = StringField(max_length=25, null=True)

    def __str__(self):
        if self.anilist is not None:
            return f"anilist: {str(self.anilist)}"
        if self.anidb is not None:
            return f"anidb: {str(self.anidb)}"
        if self.animeplanet is not None:
            return f"animeplanet: {str(self.animeplanet)}"
        if self.kitsu is not None:
            return f"kitsu: {str(self.kitsu)}"
        if self.mal is not None:
            return f"mal: {str(self.mal)}"
        if self.notify is not None:
            return f"notify: {str(self.notify)}"


class Anime(Document):
    title = StringField(max_length=256)
    source = ReferenceField(document_type=AnimeSource, reverse_delete_rule=CASCADE)
    year = IntField(null=True)
    season = StringField(max_length=12, choices=SEASON_CHOICES)
    type = StringField(max_length=12, choices=TYPE_CHOICES)
    episodes = IntField()
    status = StringField(max_length=12, choices=STATUS_CHOICES)
    picture = URLField()
    thumbnail = StringField(max_length=256,)
    synonyms = ListField(StringField(max_length=256))
    relations = ListField(URLField())
    tags = ListField(StringField(max_length=256))
    updated_at = DateTimeField(default=timezone.now().utcnow())

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("title", "updated_at")

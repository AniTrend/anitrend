from mongoengine import Document, URLField, IntField, StringField, DateField, DateTimeField, ListField, FloatField, \
    ReferenceField, CASCADE

from .choices import STATUS_CHOICES


class Image(Document):
    banner = URLField(null=True)
    poster = URLField(null=True)
    fan_art = URLField(null=True)


class Show(Document):
    tvdb_id = IntField(primary_key=True)
    title = StringField(max_length=256)
    overview = StringField(null=True)
    slug = StringField(max_length=256)
    first_aired = DateField()
    tv_maze_id = IntField(unique=True)
    added = DateTimeField()
    last_updated = DateTimeField(null=True)
    status = StringField(
        max_length=10,
        choices=STATUS_CHOICES
    )
    runtime = IntField()
    time_of_day = DateTimeField()
    network = StringField(max_length=128)
    imdb_id = StringField(max_length=128, unique=True)
    genres = ListField(
        StringField(max_length=128)
    )
    content_rating = StringField(max_length=16)
    rating = FloatField()
    alternative_titles = ListField(
        StringField(max_length=256)
    )
    image = ReferenceField(document_type=Image, reverse_delete_rule=CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("title", "last_updated", "rating", "added")


class Season(Document):
    season_number = IntField()
    show = ReferenceField(document_type=Show, reverse_delete_rule=CASCADE)
    image = ReferenceField(document_type=Image, reverse_delete_rule=CASCADE)

    def __str__(self):
        prefix = ""
        if self.season_number < 9:
            prefix = "0"
        return f"{self.show} • S{prefix}{self.season_number}"

    class Meta:
        ordering = ("season_number",)


class Episode(Document):
    tvdb_show_id = IntField(db_index=True)
    tvdb_id = IntField(db_index=True)
    season = ReferenceField(document_type=Season, on_delete=CASCADE)
    episode_number = IntField()
    aired_after_season = ReferenceField(
        document_type=Season,
        on_delete=CASCADE,
        null=True
    )
    title = StringField(max_length=256)
    air_date = DateField()
    air_date_utc = DateTimeField()
    overview = StringField(null=True)
    writers = ListField(
        StringField(max_length=256),
        null=True
    )
    directors = ListField(
        StringField(max_length=256),
        null=True
    )
    image = URLField(null=True)

    def __str__(self):
        prefix = ""
        if self.episode_number < 9:
            prefix = "0"
        return f"{self.season} - E{prefix}{self.episode_number} • {self.title}"

    class Meta:
        ordering = ("episode_number", "title")

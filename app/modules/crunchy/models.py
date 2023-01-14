from mongoengine import Document, StringField, DateTimeField, BooleanField, ListField, FloatField, \
    IntField, ReferenceField, URLField, CASCADE


class CrunchPoster(Document):
    height: IntField()
    source: URLField()
    type: StringField()
    width: IntField()


class CrunchyImage(Document):
    poster_tall = ListField(ReferenceField(document_type=CrunchPoster, reverse_delete_rule=CASCADE))
    poster_wide = ListField(ReferenceField(document_type=CrunchPoster, reverse_delete_rule=CASCADE))


class CrunchyToken(Document):
    access_token = StringField(null=True)
    expires_at = IntField()
    token_type = StringField(max_length=128)
    country = StringField(max_length=128)

    def __str__(self):
        return f"Bearer {self.access_token}"


class CrunchySigningPolicy(Document):
    bucket = StringField(max_length=64)
    policy = StringField(null=False)
    signature = StringField(null=False)
    key_pair_id = StringField(null=False)
    expires = DateTimeField()


class CrunchyIndex(Document):
    prefix = StringField(max_length=2, unique=True)
    offset = IntField()
    count = IntField()

    def __str__(self):
        return f"{self.prefix} - {self.count}"


class CrunchySeriesMeta(Document):
    audio_locales = ListField(StringField(max_length=8))
    subtitle_locales = ListField(StringField(max_length=8))
    extended_description = StringField()
    slug = StringField(max_length=480)
    title = StringField(max_length=480)
    slug_title = StringField(max_length=480)
    episode_count = IntField()
    season_count = IntField()
    is_mature = BooleanField()
    mature_blocked = BooleanField()
    is_subbed = BooleanField()
    is_dubbed = BooleanField()
    is_simulcast = BooleanField()
    maturity_ratings = ListField(StringField(max_length=24))
    tenant_categories = ListField(StringField(max_length=24), null=True)
    last_public_season_number = IntField(null=True)
    last_public_episode_number = IntField(null=True)


class CrunchyMovieMeta(Document):
    audio_locales = ListField(StringField(max_length=8))
    subtitle_locales = ListField(StringField(max_length=8))
    extended_description = StringField()
    slug = StringField(max_length=480)
    title = StringField(max_length=480)
    slug_title = StringField(max_length=480)
    duration_ms = IntField()
    movie_release_year = IntField()
    is_premium_only = BooleanField()
    is_mature = BooleanField()
    mature_blocked = BooleanField()
    is_subbed = BooleanField()
    is_dubbed = BooleanField()
    available_offline = BooleanField()
    maturity_ratings = ListField(StringField(max_length=24))
    tenant_categories = ListField(StringField(max_length=24), null=True)


class CrunchyPanel(Document):
    panel_id = StringField(max_length=24)
    external_id = StringField(max_length=24)
    channel_id = StringField(max_length=24)
    title = StringField(max_length=256)
    description = StringField(null=True)
    type = StringField(max_length=24)
    slug = StringField(max_length=128)
    images = ReferenceField(document_type=CrunchyImage, reverse_delete_rule=CASCADE, null=True)
    movie_listing_metadata = ReferenceField(document_type=CrunchyMovieMeta, reverse_delete_rule=CASCADE, null=True)
    series_metadata = ReferenceField(document_type=CrunchySeriesMeta, reverse_delete_rule=CASCADE, null=True)
    last_public = DateTimeField()
    new = BooleanField()
    new_content = BooleanField()


class CrunchyEpisode(Document):
    episode_id = StringField(max_length=128)
    index_id = IntField()
    channel_id = StringField(max_length=128)
    series_id = StringField(max_length=128)
    series_title = StringField(max_length=128)
    season_id = StringField(max_length=128)
    season_title = StringField(max_length=128)
    season_number = IntField()
    episode = StringField(max_length=128)
    episode_number = IntField(null=True)
    sequence_number = FloatField()
    production_episode_id = StringField(max_length=128)
    title = StringField(max_length=256)
    description = StringField(null=True)
    next_episode_id = StringField(max_length=24)
    next_episode_title = StringField(max_length=256)
    hd_flag = BooleanField()
    is_mature = BooleanField()
    mature_blocked = BooleanField()
    episode_air_date = DateTimeField()
    is_subbed = BooleanField()
    is_dubbed = BooleanField()
    is_clip = BooleanField()
    season_tags = ListField(StringField(max_length=128))
    available_offline = BooleanField()
    media_type = StringField(max_length=128)
    slug = StringField(max_length=128)
    images = ReferenceField(document_type=CrunchyImage, reverse_delete_rule=CASCADE, null=True)
    duration_ms = IntField(null=True)
    is_premium_only = BooleanField()
    listing_id = StringField(max_length=128)
    subtitle_locales = ListField(StringField(max_length=24))
    playback = StringField(max_length=128)


class CrunchySeason(Document):
    season_id = StringField(max_length=128)
    channel_id = StringField(max_length=128)
    title = StringField(max_length=128)
    series_id = StringField(max_length=128)
    season_number = IntField()
    is_complete = BooleanField()
    description = StringField(null=True)
    keywords = ListField(StringField(max_length=128))
    season_tags = ListField(StringField(max_length=128))
    images = ReferenceField(document_type=CrunchyImage, reverse_delete_rule=CASCADE, null=True)
    is_mature = BooleanField()
    mature_blocked = BooleanField()
    is_subbed = BooleanField()
    is_dubbed = BooleanField()
    is_simulcast = BooleanField()


class CrunchySeries(Document):
    series_id = StringField(max_length=128)
    channel_id = StringField(max_length=128)
    title = StringField(max_length=128)
    slug = StringField(max_length=128)
    description = StringField(null=True)
    keywords = ListField(StringField(max_length=128))
    season_tags = ListField(StringField(max_length=128))
    images = ReferenceField(document_type=CrunchyImage, reverse_delete_rule=CASCADE, null=True)
    maturity_ratings = ListField(StringField(max_length=128))
    episode_count = IntField()
    season_count = IntField()
    media_count = IntField()
    content_provider = StringField(max_length=128)
    is_mature = BooleanField()
    mature_blocked = BooleanField()
    is_subbed = BooleanField()
    is_dubbed = BooleanField()
    is_simulcast = BooleanField()


class CrunchyMovie(Document):
    movie_id = StringField(max_length=25)
    channel_id = StringField(max_length=25)
    title = StringField(max_length=256)
    slug = StringField(max_length=128)
    description = StringField(null=True)
    keywords = ListField(StringField(max_length=128))
    images = ReferenceField(document_type=CrunchyImage, reverse_delete_rule=CASCADE, null=True)
    maturity_ratings = ListField(StringField(max_length=128))
    season_tags = ListField(StringField(max_length=128))
    hd_flag = BooleanField()
    is_premium_only = BooleanField()
    is_mature = BooleanField()
    mature_blocked = BooleanField()
    movie_release_year = IntField()
    content_provider = StringField(max_length=128)
    is_subbed = BooleanField()
    is_dubbed = BooleanField()
    available_offline = BooleanField()

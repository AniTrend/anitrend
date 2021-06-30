from serde import Model, fields


class CrunchyToken(Model):
    access_token = fields.Str()
    expires_in = fields.Int()
    token_type = fields.Str()
    country = fields.Str()


class CrunchySigningPolicy(Model):
    bucket = fields.Str()
    policy = fields.Str()
    signature = fields.Str()
    key_pair_id = fields.Str()
    expires = fields.Str()


class CrunchySigningPolicyContainer(Model):
    cms = fields.Nested(CrunchySigningPolicy)
    service_available = fields.Bool()


class CrunchySeriesPanel(Model):
    episode_count = fields.Int()
    season_count = fields.Int()
    is_mature = fields.Bool()
    mature_blocked = fields.Bool()
    is_subbed = fields.Bool()
    is_dubbed = fields.Bool()
    is_simulcast = fields.Bool()
    maturity_ratings = fields.List(fields.Str())
    tenant_categories = fields.Optional(fields.List(fields.Str))
    last_public_season_number = fields.Optional(fields.Int())
    last_public_episode_number = fields.Optional(fields.Int())


class CrunchyMoviePanel(Model):
    duration_ms = fields.Int()
    movie_release_year = fields.Int()
    is_premium_only = fields.Bool()
    is_mature = fields.Bool()
    mature_blocked = fields.Bool()
    is_subbed = fields.Bool()
    is_dubbed = fields.Bool()
    available_offline = fields.Bool()
    maturity_ratings = fields.List(fields.Str())
    tenant_categories = fields.List(fields.Str)


class CrunchySearchMeta(Model):
    score = fields.Int()
    rank = fields.Int()
    popularity_score = fields.Float()


class CrunchyImage(Model):
    width = fields.Int()
    height = fields.Int()
    type = fields.Str()
    source = fields.Str()


class CrunchyImageContainer(Model):
    poster_tall = fields.Optional(fields.List(fields.Nested(CrunchyImage)))
    poster_wide = fields.Optional(fields.List(fields.Nested(CrunchyImage)))
    thumbnail = fields.Optional(fields.List(fields.Nested(CrunchyImage)))


class CrunchyPanel(Model):
    id = fields.Str()
    external_id = fields.Str()
    channel_id = fields.Str()
    title = fields.Str()
    description = fields.Str()
    type = fields.Str()
    slug = fields.Str()
    images = fields.Optional(fields.Nested(CrunchyImageContainer))
    movie_listing_metadata = fields.Optional(fields.Nested(CrunchyMoviePanel))
    series_metadata = fields.Optional(fields.Nested(CrunchySeriesPanel))
    search_metadata = fields.Optional(fields.Nested(CrunchySearchMeta))
    last_public = fields.Optional(fields.Str())
    new = fields.Optional(fields.Bool())
    new_content = fields.Optional(fields.Bool())


class CrunchyPanelCollection(Model):
    total = fields.Int()
    items = fields.List(fields.Nested(CrunchyPanel))


class CrunchyIndex(Model):
    prefix = fields.Str()
    offset = fields.Int()
    count = fields.Int()
    num_items = fields.Int()
    items = fields.List(fields.Nested(CrunchyPanel))


class CrunchyIndexContainer(Model):
    total_count = fields.Int()
    num_items = fields.Int()
    items = fields.List(fields.Nested(CrunchyIndex))


class CrunchyAdBreak(Model):
    type = fields.Str()
    offset_ms = fields.Int()


class CrunchyEpisode(Model):
    id = fields.Str()
    channel_id = fields.Str()
    series_id = fields.Str()
    series_title = fields.Str()
    season_id = fields.Str()
    season_title = fields.Str()
    season_number = fields.Int()
    episode = fields.Str()
    episode_number = fields.Optional(fields.Int())
    sequence_number = fields.Float()
    production_episode_id = fields.Str()
    title = fields.Str()
    description = fields.Str()
    next_episode_id = fields.Optional(fields.Str())
    next_episode_title = fields.Optional(fields.Str())
    hd_flag = fields.Bool()
    is_mature = fields.Bool()
    mature_blocked = fields.Bool()
    episode_air_date = fields.Str()
    is_subbed = fields.Bool()
    is_dubbed = fields.Bool()
    is_clip = fields.Bool()
    season_tags = fields.List(fields.Str())
    available_offline = fields.Bool()
    media_type = fields.Str()
    slug = fields.Str()
    images = fields.Optional(fields.Nested(CrunchyImageContainer))
    duration_ms = fields.Optional(fields.Int())
    ad_breaks = fields.Optional(fields.List(fields.Nested(CrunchyAdBreak)))
    is_premium_only = fields.Bool()
    listing_id = fields.Str()
    subtitle_locales = fields.List(fields.Str())
    playback = fields.Str()


class CrunchyEpisodeCollection(Model):
    total = fields.Int()
    items = fields.List(fields.Nested(CrunchyEpisode))


class CrunchySeason(Model):
    id = fields.Str()
    channel_id = fields.Str()
    title = fields.Str()
    series_id = fields.Str()
    season_number = fields.Int()
    is_complete = fields.Bool()
    description = fields.Str()
    keywords = fields.List(fields.Str())
    season_tags = fields.List(fields.Str())
    images = fields.Optional(fields.Nested(CrunchyImageContainer))
    is_mature = fields.Bool()
    mature_blocked = fields.Bool()
    is_subbed = fields.Bool()
    is_dubbed = fields.Bool()
    is_simulcast = fields.Bool()


class CrunchySeasonCollection(Model):
    total = fields.Int()
    items = fields.List(fields.Nested(CrunchySeason))


class CrunchySeries(Model):
    id = fields.Str()
    channel_id = fields.Str()
    title = fields.Str()
    slug = fields.Str()
    description = fields.Str()
    keywords = fields.List(fields.Str())
    season_tags = fields.List(fields.Str())
    images = fields.Optional(fields.Nested(CrunchyImageContainer))
    maturity_ratings = fields.List(fields.Str())
    episode_count = fields.Int()
    season_count = fields.Int()
    media_count = fields.Int()
    content_provider = fields.Str()
    is_mature = fields.Bool()
    mature_blocked = fields.Bool()
    is_subbed = fields.Bool()
    is_dubbed = fields.Bool()
    is_simulcast = fields.Bool()


class CrunchyMovie(Model):
    id = fields.Str()
    channel_id = fields.Str()
    title = fields.Str()
    slug = fields.Str()
    description = fields.Str()
    keywords = fields.List(fields.Str())
    images = fields.Optional(fields.Nested(CrunchyImageContainer))
    maturity_ratings = fields.List(fields.Str())
    season_tags = fields.List(fields.Str())
    hd_flag = fields.Bool()
    is_premium_only = fields.Bool()
    is_mature = fields.Bool()
    mature_blocked = fields.Bool()
    movie_release_year = fields.Int()
    content_provider = fields.Str()
    is_subbed = fields.Bool()
    is_dubbed = fields.Bool()
    available_offline = fields.Bool()

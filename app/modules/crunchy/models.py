from django.contrib.postgres.fields import ArrayField
from django.db import models

from ..common.models import CommonModel


class CrunchyToken(CommonModel):
    access_token = models.TextField(null=True)
    expires_at = models.IntegerField()
    token_type = models.CharField(max_length=128)
    country = models.CharField(max_length=128)


class CrunchySigningPolicy(CommonModel):
    bucket = models.CharField(max_length=64)
    policy = models.TextField(null=False)
    signature = models.TextField(null=False)
    key_pair_id = models.TextField(null=False)
    expires = models.DateTimeField()


class CrunchyIndex(CommonModel):
    prefix = models.CharField(max_length=2, unique=True)
    offset = models.IntegerField()
    count = models.IntegerField()


class CrunchySeriesPanel(CommonModel):
    episode_count = models.IntegerField()
    season_count = models.IntegerField()
    is_mature = models.BooleanField()
    mature_blocked = models.BooleanField()
    is_subbed = models.BooleanField()
    is_dubbed = models.BooleanField()
    is_simulcast = models.BooleanField()
    maturity_ratings = ArrayField(models.CharField(max_length=24))
    tenant_categories = ArrayField(models.CharField(max_length=24), null=True)
    last_public_season_number = models.IntegerField(null=True)
    last_public_episode_number = models.IntegerField(null=True)


class CrunchyMoviePanel(CommonModel):
    duration_ms = models.IntegerField()
    movie_release_year = models.IntegerField()
    is_premium_only = models.BooleanField()
    is_mature = models.BooleanField()
    mature_blocked = models.BooleanField()
    is_subbed = models.BooleanField()
    is_dubbed = models.BooleanField()
    available_offline = models.BooleanField()
    maturity_ratings = ArrayField(models.CharField(max_length=24))
    tenant_categories = ArrayField(models.CharField(max_length=24), null=True)


class CrunchyPanel(CommonModel):
    panel_id = models.CharField(max_length=24)
    external_id = models.CharField(max_length=24)
    channel_id = models.CharField(max_length=24)
    title = models.CharField(max_length=256)
    description = models.TextField(null=True)
    type = models.CharField(max_length=24)
    slug = models.SlugField(max_length=128)
    images = models.JSONField(null=True)
    movie_listing_metadata = models.OneToOneField(CrunchyMoviePanel, on_delete=models.CASCADE, null=True)
    series_metadata = models.OneToOneField(CrunchySeriesPanel, on_delete=models.CASCADE, null=True)
    last_public = models.DateTimeField()
    new = models.BooleanField()
    new_content = models.BooleanField()


class CrunchyEpisode(CommonModel):
    episode_id = models.CharField(max_length=128)
    index_id = models.IntegerField()
    channel_id = models.CharField(max_length=128)
    series_id = models.CharField(max_length=128)
    series_title = models.CharField(max_length=128)
    season_id = models.CharField(max_length=128)
    season_title = models.CharField(max_length=128)
    season_number = models.IntegerField()
    episode = models.CharField(max_length=128)
    episode_number = models.IntegerField(null=True)
    sequence_number = models.FloatField()
    production_episode_id = models.CharField(max_length=128)
    title = models.CharField(max_length=256)
    description = models.TextField(null=True)
    next_episode_id = models.CharField(max_length=24)
    next_episode_title = models.CharField(max_length=256)
    hd_flag = models.BooleanField()
    is_mature = models.BooleanField()
    mature_blocked = models.BooleanField()
    episode_air_date = models.DateTimeField()
    is_subbed = models.BooleanField()
    is_dubbed = models.BooleanField()
    is_clip = models.BooleanField()
    season_tags = ArrayField(models.CharField(max_length=128))
    available_offline = models.BooleanField()
    media_type = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    images = models.JSONField(null=True)
    duration_ms = models.IntegerField(null=True)
    is_premium_only = models.BooleanField()
    listing_id = models.CharField(max_length=128)
    subtitle_locales = ArrayField(models.CharField(max_length=24))
    playback = models.CharField(max_length=128)


class CrunchySeason(CommonModel):
    season_id = models.CharField(max_length=128)
    channel_id = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    series_id = models.CharField(max_length=128)
    season_number = models.IntegerField()
    is_complete = models.BooleanField()
    description = models.TextField(null=True)
    keywords = ArrayField(models.CharField(max_length=128))
    season_tags = ArrayField(models.CharField(max_length=128))
    images = models.JSONField(null=True)
    is_mature = models.BooleanField()
    mature_blocked = models.BooleanField()
    is_subbed = models.BooleanField()
    is_dubbed = models.BooleanField()
    is_simulcast = models.BooleanField()


class CrunchySeries(CommonModel):
    series_id = models.CharField(max_length=128)
    channel_id = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    description = models.TextField(null=True)
    keywords = ArrayField(models.CharField(max_length=128))
    season_tags = ArrayField(models.CharField(max_length=128))
    images = models.JSONField(null=True)
    maturity_ratings = ArrayField(models.CharField(max_length=128))
    episode_count = models.IntegerField()
    season_count = models.IntegerField()
    media_count = models.IntegerField()
    content_provider = models.CharField(max_length=128)
    is_mature = models.BooleanField()
    mature_blocked = models.BooleanField()
    is_subbed = models.BooleanField()
    is_dubbed = models.BooleanField()
    is_simulcast = models.BooleanField()


class CrunchyMovie(CommonModel):
    movie_id = models.CharField(max_length=25)
    channel_id = models.CharField(max_length=25)
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=128)
    description = models.TextField(null=True)
    keywords = ArrayField(models.CharField(max_length=128))
    images = models.JSONField(null=True)
    maturity_ratings = ArrayField(models.CharField(max_length=128))
    season_tags = ArrayField(models.CharField(max_length=128))
    hd_flag = models.BooleanField()
    is_premium_only = models.BooleanField()
    is_mature = models.BooleanField()
    mature_blocked = models.BooleanField()
    movie_release_year = models.IntegerField()
    content_provider = models.CharField(max_length=128)
    is_subbed = models.BooleanField()
    is_dubbed = models.BooleanField()
    available_offline = models.BooleanField()

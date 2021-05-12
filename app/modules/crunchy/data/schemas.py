import typing
from itertools import chain

from marshmallow import Schema, fields, EXCLUDE, post_load, RAISE
from marshmallow.error_store import ErrorStore
from marshmallow.fields import String, Integer, Float, Boolean, List
from marshmallow.schema import _T as T

from ...common.schemas import CommonSchema
from ..domain.entities import CrunchySigningPolicyContainer, CrunchyToken, CrunchyIndex, CrunchyPanelCollection, \
    CrunchyEpisodeCollection, CrunchySeasonCollection, CrunchyMovie, CrunchySeries


class ResourceSchema(CommonSchema):
    __class__: String = fields.Str()
    __href__: String = fields.Str()
    __resource_key__: String = fields.Str(allow_none=True, )

    @staticmethod
    def __modify_image_body(
            data: typing.Union[typing.Mapping[str, typing.Any], typing.Iterable[typing.Mapping[str, typing.Any]]]
    ) -> typing.Union[typing.Mapping[str, typing.Any], typing.Iterable[typing.Mapping[str, typing.Any]]]:
        # Images seem to be nested lists which is redundant so we're going to flatten the list
        if "images" in data:
            images = data["images"]
            if "poster_tall" in images:
                poster_tall = list(chain.from_iterable(images["poster_tall"]))
                data["images"]["poster_tall"] = poster_tall
            if "poster_wide" in images:
                poster_wide = list(chain.from_iterable(images["poster_wide"]))
                data["images"]["poster_wide"] = poster_wide
            if "thumbnail" in images:
                thumbnail = list(chain.from_iterable(images["thumbnail"]))
                data["images"]["thumbnail"] = thumbnail
        return data

    def _deserialize(
            self,
            data: typing.Union[
                typing.Mapping[str, typing.Any],
                typing.Iterable[typing.Mapping[str, typing.Any]],
            ], *,
            error_store: ErrorStore,
            many: bool = False,
            partial=False,
            unknown=RAISE,
            index=None
    ) -> typing.Union[T, typing.List[T]]:
        return super()._deserialize(
            self.__modify_image_body(data),
            error_store=error_store,
            many=many,
            partial=partial,
            unknown=unknown,
            index=index
        )


class TokenSchema(CommonSchema):
    bucket: String = fields.Str()
    access_token: String = fields.Str()
    expires_in: Integer = fields.Int()
    token_type: String = fields.Str()
    country: String = fields.Str()

    @post_load()
    def __on_post_load(self, data, many, **kwargs) -> CrunchyToken:
        try:
            model = CrunchyToken.from_dict(data)
            return model
        except Exception as e:
            self._logger.error(f"Conversion from dictionary failed", exc_info=e)
            raise e


class SigningPolicySchema(CommonSchema):
    bucket: String = fields.Str()
    policy: String = fields.Str()
    signature: String = fields.Str()
    key_pair_id: String = fields.Str()
    expires: String = fields.Str()


class SigningPolicyContainerSchema(CommonSchema):
    cms: SigningPolicySchema = fields.Nested(
        nested=SigningPolicySchema,
    )
    service_available: Boolean = fields.Boolean()

    @post_load()
    def __on_post_load(self, data, many, **kwargs) -> CrunchySigningPolicyContainer:
        try:
            model = CrunchySigningPolicyContainer.from_dict(data)
            return model
        except Exception as e:
            self._logger.error(f"Conversion from dictionary failed", exc_info=e)
            raise e


class IndexSchema(CommonSchema):
    prefix: String = fields.Str()
    offset: Integer = fields.Int()
    count: Integer = fields.Int()


class IndexContainerSchema(ResourceSchema):
    total_count: Integer = fields.Int()
    num_items: Integer = fields.Int()
    items = fields.List(
        fields.Nested(
            nested=IndexSchema,
            allow_none=True,
            unknown=EXCLUDE
        )
    )

    @post_load()
    def __on_post_load(self, data, many, **kwargs) -> CrunchyIndex:
        try:
            model = CrunchyIndex.from_dict(data)
            return model
        except Exception as e:
            self._logger.error(f"Conversion from dictionary failed", exc_info=e)
            raise e


class SeriesPanelMetaSchema(CommonSchema):
    episode_count: Integer = fields.Int()
    season_count: Integer = fields.Int()
    is_mature: Boolean = fields.Bool()
    mature_blocked: Boolean = fields.Bool()
    is_subbed: Boolean = fields.Bool()
    is_dubbed: Boolean = fields.Bool()
    is_simulcast: Boolean = fields.Bool()
    maturity_ratings: List = fields.List(fields.Str())
    tenant_categories: List = fields.List(fields.Str)
    last_public_season_number: Integer = fields.Int()
    last_public_episode_number: Integer = fields.Int()


class MoviePanelMetaSchema(CommonSchema):
    duration_ms: Integer = fields.Int()
    movie_release_year: Integer = fields.Int()
    is_premium_only: Boolean = fields.Bool()
    is_mature: Boolean = fields.Bool()
    mature_blocked: Boolean = fields.Bool()
    is_subbed: Boolean = fields.Bool()
    is_dubbed: Boolean = fields.Bool()
    available_offline: Boolean = fields.Bool()
    maturity_ratings: List = fields.List(fields.Str())
    tenant_categories: List = fields.List(fields.Str)


class SearchMetaSchema(CommonSchema):
    score: Integer = fields.Int()
    rank: Integer = fields.Int()
    popularity_score: Float = fields.Float()


class ImageSchema(CommonSchema):
    width: Integer = fields.Int()
    height: Integer = fields.Int()
    type: String = fields.Str()
    source: String = fields.Str()


class ImageContainerSchema(CommonSchema):
    poster_tall: List = fields.List(
        fields.Nested(
            nested=ImageSchema,
            allow_none=True,
            unknown=EXCLUDE,

        )
    )
    poster_wide: List = fields.List(
        fields.Nested(
            nested=ImageSchema,
            allow_none=True,
            unknown=EXCLUDE,

        )
    )
    thumbnail: List = fields.List(
        fields.Nested(
            nested=ImageSchema,
            allow_none=True,
            unknown=EXCLUDE,

        )
    )


class PanelSchema(ResourceSchema):
    id: String = fields.Str()
    external_id: String = fields.Str()
    channel_id: String = fields.Str()
    title: String = fields.Str()
    description: String = fields.Str()
    type: String = fields.Str()
    slug: String = fields.Str()
    images = fields.Nested(
        nested=ImageContainerSchema,
        allow_none=True,
        unknown=EXCLUDE,

    )
    movie_listing_metadata = fields.Nested(
        nested=MoviePanelMetaSchema,
        allow_none=True,
        unknown=EXCLUDE,

    )
    series_metadata = fields.Nested(
        nested=SeriesPanelMetaSchema,
        allow_none=True,
        unknown=EXCLUDE,

    )
    locale: String = fields.Str()
    search_metadata = fields.Nested(
        nested=SearchMetaSchema,
        allow_none=True,
        unknown=EXCLUDE,

    )
    last_public: String = fields.Str(allow_none=True)
    new: Boolean = fields.Bool()
    new_content: Boolean = fields.Bool()


class CollectionContainerSchema(ResourceSchema):
    total: Integer = fields.Int()
    items: List = fields.List(
        fields.Nested(
            nested=PanelSchema,
            unknown=EXCLUDE,
        )
    )

    @post_load()
    def __on_post_load(self, data, many, **kwargs) -> CrunchyPanelCollection:
        try:
            model = CrunchyPanelCollection.from_dict(data)
            return model
        except Exception as e:
            self._logger.error(f"Conversion from dictionary failed", exc_info=e)
            raise e


class AdBreakSchema(CommonSchema):
    type: String = fields.Str()
    offset_ms: Integer = fields.Int()


class EpisodeSchema(ResourceSchema):
    id: String = fields.Str()
    channel_id: String = fields.Str()
    series_id: String = fields.Str()
    series_title: String = fields.Str()
    season_id: String = fields.Str()
    season_title: String = fields.Str()
    season_number: Integer = fields.Int()
    episode: String = fields.Str()
    episode_number: Integer = fields.Int(allow_none=True)
    sequence_number: Integer = fields.Int(strict=False)
    production_episode_id: String = fields.Str()
    title: String = fields.Str()
    description: String = fields.Str()
    next_episode_id: String = fields.Str(allow_none=True)
    next_episode_title: String = fields.Str(allow_none=True)
    hd_flag: Boolean = fields.Bool()
    is_mature: Boolean = fields.Bool()
    mature_blocked: Boolean = fields.Bool()
    episode_air_date: String = fields.Str()
    is_subbed: Boolean = fields.Bool()
    is_dubbed: Boolean = fields.Bool()
    is_clip: Boolean = fields.Bool()
    season_tags: List = fields.List(fields.Str())
    available_offline: Boolean = fields.Bool()
    media_type: String = fields.Str()
    slug: String = fields.Str()
    images = fields.Nested(
        nested=ImageContainerSchema,
        allow_none=True,
        unknown=EXCLUDE,
    )
    duration_ms: Integer = fields.Int(allow_none=True)
    ad_breaks = fields.List(
        fields.Nested(
            nested=AdBreakSchema,
            allow_none=True,
            unknown=EXCLUDE,
        )
    )
    is_premium_only: Boolean = fields.Bool()
    listing_id: String = fields.Str()
    subtitle_locales: List = fields.List(fields.Str())
    playback: String = fields.Str()


class EpisodeContainerSchema(ResourceSchema):
    total: Integer = fields.Int()
    items: List = fields.List(
        fields.Nested(
            nested=EpisodeSchema,
            allow_none=True,
            unknown=EXCLUDE,
        )
    )

    @post_load()
    def __on_post_load(self, data, many, **kwargs) -> CrunchyEpisodeCollection:
        try:
            model = CrunchyEpisodeCollection.from_dict(data)
            return model
        except Exception as e:
            self._logger.error(f"Conversion from dictionary failed", exc_info=e)
            raise e


class SeasonSchema(ResourceSchema):
    id: String = fields.Str()
    channel_id: String = fields.Str()
    title: String = fields.Str()
    series_id: String = fields.Str()
    season_number: Integer = fields.Int()
    is_complete: Boolean = fields.Bool()
    description: String = fields.Str()
    keywords: List = fields.List(fields.Str())
    season_tags: List = fields.List(fields.Str())
    images = fields.Nested(
        nested=ImageContainerSchema,
        allow_none=True,
        unknown=EXCLUDE,

    )
    is_mature: Boolean = fields.Bool()
    mature_blocked: Boolean = fields.Bool()
    is_subbed: Boolean = fields.Bool()
    is_dubbed: Boolean = fields.Bool()
    is_simulcast: Boolean = fields.Bool()


class SeasonContainerSchema(ResourceSchema):
    total: Integer = fields.Int()
    items: List = fields.List(
        fields.Nested(
            nested=SeasonSchema,
            allow_none=True,
            unknown=EXCLUDE,

        )
    )

    @post_load()
    def __on_post_load(self, data, many, **kwargs) -> CrunchySeasonCollection:
        try:
            model = CrunchySeasonCollection.from_dict(data)
            return model
        except Exception as e:
            self._logger.error(f"Conversion from dictionary failed", exc_info=e)
            raise e


class SeriesSchema(ResourceSchema):
    id: String = fields.Str()
    channel_id: String = fields.Str()
    title: String = fields.Str()
    slug: String = fields.Str()
    description: String = fields.Str()
    keywords: List = fields.List(fields.Str())
    season_tags: List = fields.List(fields.Str())
    images = fields.Nested(
        nested=ImageContainerSchema,
        allow_none=True,
        unknown=EXCLUDE,
    )
    maturity_ratings: List = fields.List(fields.Str())
    episode_count: Integer = fields.Int()
    season_count: Integer = fields.Int()
    media_count: Integer = fields.Int()
    content_provider: String = fields.Str()
    is_mature: Boolean = fields.Bool()
    mature_blocked: Boolean = fields.Bool()
    is_subbed: Boolean = fields.Bool()
    is_dubbed: Boolean = fields.Bool()
    is_simulcast: Boolean = fields.Bool()

    @post_load()
    def __on_post_load(self, data, many, **kwargs) -> CrunchySeries:
        try:
            model = CrunchySeries.from_dict(data)
            return model
        except Exception as e:
            self._logger.error(f"Conversion from dictionary failed", exc_info=e)
            raise e


class MovieSchema(ResourceSchema):
    id: String = fields.Str()
    channel_id: String = fields.Str()
    title: String = fields.Str()
    slug: String = fields.Str()
    description: String = fields.Str()
    keywords: List = fields.List(fields.Str())
    images = fields.Nested(
        nested=ImageContainerSchema,
        allow_none=True,
        unknown=EXCLUDE,

    )
    maturity_ratings: List = fields.List(fields.Str())
    season_tags: List = fields.List(fields.Str())
    hd_flag: Boolean = fields.Bool()
    is_premium_only: Boolean = fields.Bool()
    is_mature: Boolean = fields.Bool()
    mature_blocked: Boolean = fields.Bool()
    movie_release_year: Integer = fields.Int()
    content_provider: String = fields.Str()
    is_subbed: Boolean = fields.Bool()
    is_dubbed: Boolean = fields.Bool()
    available_offline: Boolean = fields.Bool()

    @post_load()
    def __on_post_load(self, data, many, **kwargs) -> CrunchyMovie:
        try:
            model = CrunchyMovie.from_dict(data)
            return model
        except Exception as e:
            self._logger.error(f"Conversion from dictionary failed", exc_info=e)
            raise e

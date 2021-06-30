from marshmallow import fields, post_load, EXCLUDE

from ...common.schemas import CommonSchema
from ..domain.entities import SkyhookShow


class Image(CommonSchema):
    coverType = fields.Str()
    url = fields.Str()


class Episode(CommonSchema):
    tvdbShowId = fields.Int()
    tvdbId = fields.Int()
    seasonNumber = fields.Int()
    episodeNumber = fields.Int()
    airedAfterSeasonNumber = fields.Int(allow_none=True)
    title = fields.Str()
    airDate = fields.Str()
    airDateUtc = fields.Str()
    overview = fields.Str(allow_none=True)
    writers = fields.List(fields.Str(allow_none=True))
    directors = fields.List(fields.Str(allow_none=True))
    image = fields.Str(allow_none=True)


class Season(CommonSchema):
    seasonNumber = fields.Int()
    images = fields.List(fields.Nested(Image))


class TimeOfDay(CommonSchema):
    hours = fields.Int()
    minutes = fields.Int()


class Rating(CommonSchema):
    count = fields.Int()
    value = fields.Str()


class Title(CommonSchema):
    title = fields.Str()


class Show(CommonSchema):
    tvdbId = fields.Int()
    title = fields.Str()
    overview = fields.Str()
    slug = fields.Str()
    firstAired = fields.Str()
    tvMazeId = fields.Int()
    added = fields.Str()
    lastUpdated = fields.Str()
    status = fields.Str()
    runtime = fields.Int()
    timeOfDay = fields.Nested(
        nested=TimeOfDay,
        allow_none=False,
        unknown=EXCLUDE
    )
    network = fields.Str()
    imdbId = fields.Str()
    genres = fields.List(fields.Str())
    contentRating = fields.Str()
    rating = fields.Nested(
        nested=Rating,
        allow_none=False,
        unknown=EXCLUDE
    )
    alternativeTitles = fields.List(
        fields.Nested(
            nested=Title,
            allow_none=False,
            unknown=EXCLUDE
        )
    )
    images = fields.List(
        fields.Nested(
            nested=Image,
            allow_none=False,
            unknown=EXCLUDE
        )
    )
    seasons = fields.List(
        fields.Nested(
            nested=Season,
            allow_none=False,
            unknown=EXCLUDE
        )
    )
    episodes = fields.List(
        fields.Nested(
            nested=Episode,
            allow_none=False,
            unknown=EXCLUDE
        )
    )

    @post_load()
    def __on_post_load(self, data, many, **kwargs) -> SkyhookShow:
        try:
            model = SkyhookShow.from_dict(data)
            return model
        except Exception as e:
            self._logger.error(f"Conversion from dictionary failed", exc_info=e)

from marshmallow import fields, post_load, EXCLUDE

from ...common.schemas import CommonSchema
from ..domain.entities import AnimeContainer


class Season(CommonSchema):
    season = fields.Str()
    year = fields.Int(allow_none=True)


class Data(CommonSchema):
    sources = fields.List(
        fields.Str(),
        allow_none=True,
    )
    title = fields.Str()
    type = fields.Str()
    episodes = fields.Int(allow_none=True)
    status = fields.Str()
    animeSeason = fields.Nested(
        nested=Season,
        allow_none=True,
        unknown=EXCLUDE
    )
    picture = fields.Str(allow_none=True)
    thumbnail = fields.Str(allow_none=True)
    synonyms = fields.List(
        fields.Str(),
        allow_none=True,
    )
    relations = fields.List(
        fields.Str(),
        allow_none=True,
    )
    tags = fields.List(
        fields.Str(),
        allow_none=True,
    )


class Container(CommonSchema):
    data = fields.List(
        fields.Nested(
            nested=Data,
            allow_none=False,
            unknown=EXCLUDE
        )
    )

    @post_load()
    def __on_post_load(self, data, many, **kwargs) -> AnimeContainer:
        try:
            model = AnimeContainer.from_dict(data)
            return model
        except Exception as e:
            self._logger.error(f"Conversion from dictionary failed", exc_info=e)

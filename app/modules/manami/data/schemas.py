from marshmallow import fields, post_load, EXCLUDE
from marshmallow.fields import String, List, Nested, Int

from ...common.schemas import CommonSchema
from ..domain.entities import AnimeContainer


class Season(CommonSchema):
    season: String = fields.Str()
    year: Int = fields.Int(allow_none=True)


class Data(CommonSchema):
    sources: List = fields.List(
        fields.Str(),
        allow_none=True,
    )
    title: String = fields.Str()
    type: String = fields.Str()
    episodes: Int = fields.Int(allow_none=True)
    status: String = fields.Str()
    animeSeason: Nested = fields.Nested(
        nested=Season,
        allow_none=True,
        unknown=EXCLUDE
    )
    picture: String = fields.Str(allow_none=True)
    thumbnail: String = fields.Str(allow_none=True)
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
    data: List = fields.List(
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

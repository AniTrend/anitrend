import typing
from logging import Logger
from typing import Any

from marshmallow import Schema, fields, EXCLUDE, post_load, types
from marshmallow.fields import String, Dict, List, Nested, Int

from di import MainContainer
from .model_entities import XemContainerEntity, RelationContainerEntity


class CommonSchema(Schema):
    _logger: Logger

    def __init__(self, *, only: typing.Optional[types.StrSequenceOrSet] = None, exclude: types.StrSequenceOrSet = (),
                 many: bool = False, context: typing.Optional[typing.Dict] = None,
                 load_only: types.StrSequenceOrSet = (), dump_only: types.StrSequenceOrSet = (),
                 partial: typing.Union[bool, types.StrSequenceOrSet] = False, unknown: typing.Optional[str] = None):
        super().__init__(only=only, exclude=exclude, many=many, context=context, load_only=load_only,
                         dump_only=dump_only, partial=partial, unknown=unknown)
        self._logger = MainContainer.logging_utility().get_default_logger(__name__)

    def _on_post_load(self, data, many, **kwargs) -> Any:
        pass


class XemContainer(CommonSchema):
    result: String = fields.Str()
    data: Dict = fields.Dict()
    message: String = fields.Str()

    @post_load()
    def _on_post_load(self, data, many, **kwargs) -> XemContainerEntity:
        try:
            entity = XemContainerEntity.from_dict(data)
            return entity
        except Exception as e:
            self._logger.error(f"Conversion from dictionary failed", exc_info=e)


class RelationSeason(CommonSchema):
    season: String = fields.Str()
    year: Int = fields.Int(allow_none=True)


class RelationData(CommonSchema):
    sources: List = fields.List(
        fields.Str(),
        allow_none=True,
    )
    title: String = fields.Str()
    type: String = fields.Str()
    episodes: Int = fields.Int(allow_none=True)
    status: String = fields.Str()
    animeSeason: Nested = fields.Nested(
        nested=RelationSeason,
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


class RelationContainer(CommonSchema):
    data: List = fields.List(
        fields.Nested(
            nested=RelationData,
            allow_none=False,
            unknown=EXCLUDE
        )
    )

    @post_load()
    def __on_post_load(self, data, many, **kwargs) -> RelationContainerEntity:
        try:
            entity = RelationContainerEntity.from_dict(data)
            return entity
        except Exception as e:
            self._logger.error(f"Conversion from dictionary failed", exc_info=e)

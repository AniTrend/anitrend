from typing import Any

from marshmallow import Schema, fields, EXCLUDE, post_load
from marshmallow.fields import String, Dict, List, Nested, Int

from .model_entities import XemContainerEntity, RelationContainerEntity, RelationSeasonEntity, RelationDataEntity


class CommonSchema(Schema):

    def _on_post_load(self, data, many, **kwargs) -> Any:
        pass


class XemContainer(CommonSchema):
    result: String = fields.Str()
    data: Dict = fields.Dict()
    message: String = fields.Str()

    @post_load()
    def _on_post_load(self, data, many, **kwargs) -> XemContainerEntity:
        entity = XemContainerEntity.from_dict(data)
        return entity


class RelationSeason(CommonSchema):
    season: String = fields.Str()
    year: Int = fields.Int(allow_none=True)

    @post_load()
    def _on_post_load(self, data, many, **kwargs) -> RelationSeasonEntity:
        entity = RelationSeasonEntity.from_dict(data)
        return entity


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

    @post_load()
    def _on_post_load(self, data, many, **kwargs) -> RelationDataEntity:
        entity = RelationDataEntity.from_dict(data)
        return entity


class RelationContainer(CommonSchema):
    data: Nested = fields.Nested(
        nested=RelationData,
        allow_none=False,
        unknown=EXCLUDE
    )

    @post_load()
    def _on_post_load(self, data, many, **kwargs) -> RelationContainerEntity:
        entity = RelationContainerEntity.from_dict(data)
        return entity

from marshmallow import fields, post_load
from marshmallow.fields import String, Dict

from ...common.schemas import CommonSchema
from ..domain.entities import XemContainer


class Container(CommonSchema):
    result: String = fields.Str()
    data: Dict = fields.Dict()
    message: String = fields.Str()

    @post_load()
    def _on_post_load(self, data, many, **kwargs) -> XemContainer:
        try:
            model = XemContainer.from_dict(data)
            return model
        except Exception as e:
            self._logger.error(f"Conversion from dictionary failed", exc_info=e)

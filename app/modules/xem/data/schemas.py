from marshmallow import fields, post_load

from ...common.schemas import CommonSchema
from ..domain.entities import XemContainer


class Container(CommonSchema):
    result = fields.Str()
    data = fields.Dict()
    message = fields.Str()

    @post_load()
    def _on_post_load(self, data, many, **kwargs) -> XemContainer:
        try:
            model = XemContainer.from_dict(data)
            return model
        except Exception as e:
            self._logger.error(f"Conversion from dictionary failed", exc_info=e)

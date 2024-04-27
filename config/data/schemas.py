from typing import Any

from marshmallow import fields, post_load

from config.domain.entities import ConfigurationModel
from core.schemas import CommonSchema


class SettingsSchema(CommonSchema):
    analyticsEnabled = fields.Boolean(required=True)
    platformSource = fields.String(allow_none=True)


class ImageSchema(CommonSchema):
    banner = fields.String(required=True)
    poster = fields.String(required=True)
    loading = fields.String(required=True)
    error = fields.String(required=True)
    info = fields.String(required=True)
    default = fields.String(required=True)


class NavigationGroupSchema(CommonSchema):
    authenticated = fields.Boolean(required=True)
    i18n = fields.String(required=True)


class NavigationSchema(CommonSchema):
    criteria = fields.String(required=True)
    destination = fields.String(required=True)
    i18n = fields.String(required=True)
    icon = fields.String(required=True)
    group = fields.Nested(NavigationGroupSchema(), required=True)


class GenreSchema(CommonSchema):
    name = fields.String(required=True)
    mediaId = fields.Integer(required=True)


class ConfigurationSchema(CommonSchema):
    settings = fields.Nested(SettingsSchema(), required=True)
    image = fields.Nested(ImageSchema(), allow_none=True)
    navigation = fields.List(fields.Nested(nested=NavigationSchema(), allow_none=True))
    genres = fields.List(fields.Nested(nested=GenreSchema(), allow_none=True))

    @post_load()
    def __on_post_load(self, data, many, **kwargs) -> ConfigurationModel:
        try:
            model = ConfigurationModel.from_dict(data)
            return model
        except Exception as e:
            self._logger.error(f"Conversion from dictionary failed", exc_info=e)
            raise e

from marshmallow import Schema, fields, post_load

from news.domain.entities import NewsConnectionModel


class NewsSchema(Schema):
    id = fields.String(required=True)
    title = fields.String(required=True)
    author = fields.String(required=True)
    description = fields.String(required=True)
    content = fields.String(required=True)
    image = fields.String(allow_none=True)
    published_on = fields.Integer(required=True, data_key="publishedOn")
    link = fields.String(required=True)

class NewsConnectionSchema(Schema):
    count = fields.Integer(required=True)
    first = fields.String(required=True)
    last = fields.String(required=True)
    data = fields.List(fields.Nested(NewsSchema), required=True)

    @post_load()
    def __on_post_load(self, data, many, **kwargs) -> NewsConnectionModel:
        try:
            model = NewsConnectionModel.from_dict(data)
            return model
        except Exception as e:
            self._logger.error(f"Conversion from dictionary failed", exc_info=e)
            raise e
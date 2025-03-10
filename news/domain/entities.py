from serde import fields, Model


class NewsModel(Model):
    id = fields.Str()
    title = fields.Str()
    author = fields.Str()
    description = fields.Str()
    content = fields.Str()
    image = fields.Optional(fields.Str())
    published_on = fields.Int()
    link = fields.Str()


class NewsConnectionModel(Model):
    count = fields.Int()
    first = fields.Str()
    last = fields.Str()
    data = fields.List(fields.Nested(NewsModel))
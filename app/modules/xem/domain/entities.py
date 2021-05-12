from serde import Model, fields


class XemContainer(Model):
    result = fields.Str()
    data = fields.Dict()
    message = fields.Str()

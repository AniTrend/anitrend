from serde import fields, Model


class SettingsModel(Model):
    analyticsEnabled = fields.Bool()
    platformSource = fields.Optional(fields.Str())


class ImageModel(Model):
    banner = fields.Str()
    poster = fields.Str()
    loading = fields.Str()
    error = fields.Str()
    info = fields.Str()
    default = fields.Str()


class NavigationGroupModel(Model):
    authenticated = fields.Bool()
    i18n = fields.Str()


class NavigationModel(Model):
    criteria = fields.Str()
    destination = fields.Str()
    i18n = fields.Str()
    icon = fields.Str()
    group = fields.Nested(NavigationGroupModel)


class GenreModel(Model):
    name = fields.Str()
    mediaId = fields.Int()


class ConfigurationModel(Model):
    settings = fields.Nested(SettingsModel)
    image = fields.Optional(fields.Nested(ImageModel))
    navigation = fields.Optional(fields.List(fields.Nested(NavigationModel)))
    genres = fields.Optional(fields.List(fields.Nested(GenreModel)))

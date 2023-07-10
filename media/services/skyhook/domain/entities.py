from serde import Model, fields


class SkyhookImage(Model):
    coverType = fields.Str()
    url = fields.Str()


class SkyhookEpisode(Model):
    tvdbShowId = fields.Int()
    tvdbId = fields.Int()
    seasonNumber = fields.Int()
    episodeNumber = fields.Int()
    airedAfterSeasonNumber = fields.Optional(fields.Int())
    title = fields.Str()
    airDate = fields.Str()
    airDateUtc = fields.Str()
    overview = fields.Optional(fields.Str())
    writers = fields.Optional(fields.List(fields.Str()))
    directors = fields.Optional(fields.List(fields.Str()))
    image = fields.Optional(fields.Str())


class SkyhookSeason(Model):
    seasonNumber = fields.Int()
    images = fields.List(fields.Nested(SkyhookImage))


class SkyhookTimeOfDay(Model):
    hours = fields.Int()
    minutes = fields.Int()


class SkyhookRating(Model):
    count = fields.Int()
    value = fields.Str()


class SkyhookTitle(Model):
    title = fields.Str()


class SkyhookShow(Model):
    tvdbId = fields.Int()
    title = fields.Str()
    overview = fields.Str()
    slug = fields.Str()
    firstAired = fields.Str()
    tvMazeId = fields.Int()
    added = fields.Str()
    lastUpdated = fields.Str()
    status = fields.Str()
    runtime = fields.Int()
    timeOfDay = fields.Nested(SkyhookTimeOfDay)
    network = fields.Str()
    imdbId = fields.Str()
    genres = fields.List(fields.Str())
    contentRating = fields.Str()
    rating = fields.Nested(SkyhookRating)
    alternativeTitles = fields.List(fields.Nested(SkyhookTitle))
    images = fields.List(fields.Nested(SkyhookImage))
    seasons = fields.List(fields.Nested(SkyhookSeason))
    episodes = fields.List(fields.Nested(SkyhookEpisode))

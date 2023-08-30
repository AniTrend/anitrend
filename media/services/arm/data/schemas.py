from core.schemas import CommonSchema
from marshmallow import Schema, fields


class ArmModelSchema(CommonSchema):
    anidb = fields.Integer(allow_none=True)
    anilist = fields.Integer(allow_none=True)
    anime_planet = fields.String(allow_none=True, data_key='anime-planet')
    anisearch = fields.Integer(allow_none=True)
    imdb = fields.String(allow_none=True)
    kitsu = fields.Integer(allow_none=True)
    livechart = fields.Integer(allow_none=True)
    notify_moe = fields.String(allow_none=True, data_key='notify-moe')
    themoviedb = fields.Integer(allow_none=True)
    thetvdb = fields.Integer(allow_none=True)
    myanimelist = fields.Integer(allow_none=True)

# coding=utf-8
from marshmallow import Schema, fields

from models import User, session
from config import DOMAIN


def gen_pic_url(path):
    if not path.startswith('/'):
        path = '/' + path
    return '{}{}'.format(DOMAIN, path)


class UserSchema(Schema):
    id = fields.Integer()
    url = fields.Str()
    name = fields.Str()
    headline = fields.Str()
    avatar_url = fields.Method('get_avatar_url', allow_none=True)
    live_count = fields.Integer()

    def get_avatar_url(self, obj):
        return gen_pic_url(obj.avatar_url)


class UserFullSchema(UserSchema):
    lives_url = fields.Str()
    speaker_id = fields.Str()
    gender = fields.Integer()
    bio = fields.Str()
    description = fields.Str()


class LiveSchema(Schema):
    id = fields.Str()
    url = fields.Str()
    speaker = fields.Nested(UserSchema)
    subject = fields.Str()
    feedback_score = fields.Float()
    amount = fields.Float()
    seats_taken = fields.Integer()
    topics = fields.List(fields.String)


class LiveFullSchema(LiveSchema):
    speaker = fields.Nested(UserFullSchema)
    description = fields.Str()
    status = fields.Boolean()  # public(True)/ended(False)
    starts_at = fields.Method('get_start_time')
    outline = fields.Str()
    speaker_message_count = fields.Integer()
    tag_names = fields.Str()
    liked_num = fields.Integer()
    cover = fields.Method('get_cover_url', allow_none=True)
    zhuanlan = fields.Str(allow_none=True)

    def get_start_time(self, obj):
        return int(obj['starts_at'].strftime('%s'))

    def get_cover_url(self, obj):
        return gen_pic_url(obj.get('cover', '/static/images/default-cover.png'))  # noqa

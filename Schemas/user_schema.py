from marshmallow import fields

from ma import ma
from Models.user import User


class UserSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    surname = fields.Str()
    email = fields.Email(required=True, error_messages={"required": "Email is required."})
    country = fields.Str()
    is_admin = fields.Bool(required=True, default=False)
    password_hash = fields.Str(required=True)

    class Meta:
        fields = ("id", "name", "surname", "email", "country","is_admin", "password_hash")
        model = User


user_schema = UserSchema()
users_schema = UserSchema(many=True)

from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    username = fields.String(required=True)
    default_currency_id = fields.String()
    password = fields.String(required=True)

class CategorySchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)

class RecordSchema(Schema):
    id = fields.String(dump_only=True)
    user_id = fields.String(required=True)
    category_id = fields.String(required=True)
    currency_id = fields.String()
    timestamp = fields.DateTime(dump_only=True)
    amount = fields.Float(required=True)

class CurrencySchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)

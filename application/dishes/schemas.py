from marshmallow import Schema, fields


class DishSchema_post(Schema):
    name = fields.String(required=True)
    description = fields.String()
    img_path = fields.String()
    ingredients = fields.Dict()


class DishSchema_put(Schema):
    id = fields.Int(required=True)
    name = fields.String()
    description = fields.String()
    img_path = fields.String()
    ingredients = fields.Dict()


class DishSchema_delete(Schema):
    id = fields.Int(required=True)
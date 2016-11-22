from marshmallow import Schema, fields


class ProductSchema_post(Schema):
    name = fields.String(required=True)
    quantity = fields.Int(required=True)
    ingredient_id = fields.Int(required=True)
    suppliers = fields.Dict(required=True)


class ProductSchema_put(Schema):
    id = fields.Int(required=True)
    name = fields.String()
    quantity = fields.Int()
    ingredient_id = fields.Int()
    suppliers = fields.Dict()


class ProductSchema_delete(Schema):
    id = fields.Int(required=True)

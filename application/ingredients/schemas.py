from marshmallow import Schema, fields

from ..products.schemas import ProductSchema


class CategorySchema(Schema):
    id = fields.Int()
    name = fields.String()


class IngredientSchema(Schema):
    id = fields.Int()
    name = fields.String()
    description = fields.String()
    img_path = fields.String()
    categories = fields.Nested(CategorySchema, many=True)
    products = fields.Nested(ProductSchema, many=True)
    dimension = fields.String()


class IngredientListSchema(Schema):
    quantity = fields.Int()
    ingredient = fields.Nested(IngredientSchema)
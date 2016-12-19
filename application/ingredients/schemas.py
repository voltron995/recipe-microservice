from marshmallow import Schema, fields, post_load, validate
from marshmallow.exceptions import ValidationError

from ..products.schemas import ProductSchema


class CategorySchema(Schema):
    id = fields.Int()
    name = fields.String()


class IngredientSchema(Schema):
    id = fields.Int()
    name = fields.String()
    description = fields.String()
    image = fields.String()
    categories = fields.Nested(CategorySchema, many=True)
    products = fields.Nested(ProductSchema, many=True)
    dimension = fields.String()


class IngredientListSchema(Schema):
    quantity = fields.Int(required=True)
    ingredient = fields.Nested(IngredientSchema,
        required=True
    )

    @post_load
    def check_id(self, data):
        if 'id' not in data['ingredient']:
            raise ValidationError('Ingredient must have a "id" key.')
        return data

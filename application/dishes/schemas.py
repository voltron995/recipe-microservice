from marshmallow import Schema, fields

from ..ingredients.schemas import IngredientListSchema


class DishSchema(Schema):
    id = fields.Int()
    name = fields.String()
    description = fields.String()
    img_path = fields.String()
    ingredients = fields.Nested(
        IngredientListSchema, 
        attribute='ingredients_list',
        many=True
    )
    price = fields.String(dump_only=True, attribute='price')

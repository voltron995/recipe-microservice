from marshmallow import Schema, fields

from ..ingredients.schemas import IngredientListSchema


class CategorySchema(Schema):
    id = fields.Int()
    name = fields.String()


class RecipeSchema(Schema):
    id = fields.Int()
    name = fields.String()
    description = fields.String()
    img_path = fields.String()
    categories = fields.Nested(CategorySchema, many=True)
    ingredients = fields.Nested(
    	IngredientListSchema, 
    	attribute='ingredients_list',
    	many=True)
    price = fields.String(dump_only=True, attribute='price')
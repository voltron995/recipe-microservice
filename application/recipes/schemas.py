from marshmallow import Schema, fields, pre_load, validate
from marshmallow.exceptions import ValidationError
from ..ingredients.schemas import IngredientListSchema
from .models import Recipe

class CategorySchema(Schema):
    id = fields.Int()
    name = fields.String()


class RecipeSchema(Schema):
    id = fields.Int()
    name = fields.String(required=True)
    description = fields.String()
    img_path = fields.String()
    categories = fields.Nested(CategorySchema, many=True)
    ingredients = fields.Nested(
    	IngredientListSchema,
    	attribute='ingredients_list',
    	many=True,
        required=True)
    price = fields.String(dump_only=True, attribute='price')

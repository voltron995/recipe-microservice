from marshmallow import Schema, fields, pre_load, post_dump

from ..recipes.models import *


# class IngredientCategorySchema(Schema):
#     id = fields.Number(required=True)
#     name = fields.String(required=True)
#     slug = fields.String()
# class IngredientSchema(Schema):
#     id = fields.Number(required=True)
#     name = fields.String(required=True)
#     description = fields.Str()
#     dimension = fields.String(required=True)
#     categories = fields.Nested(IngredientCategorySchema, many=True, required=True)
# class RecipeIngredientSchema(Schema):
#     recipe_id = fields.Number()
#     ingredient_id = fields.Number()
#     quantity = fields.Number()
#     ingredients = fields.Nested(IngredientSchema,many=True, only=["name","dimension"])
#
class RecipeCategorySchema(Schema):
    id = fields.Int(required=True)
    name = fields.String(required=True)
    slug = fields.String()
class RecipeSchema(Schema):
    id = fields.Number()
    name = fields.String(required=True)
    description = fields.String()
    img_path = fields.String()
    categories = fields.Method("gen_categories_list",required=True)
    ingredients = fields.Method('gen_ingredients_list', required=True)







class CategorySchema:
    post = {
        "type": "object",
        "properties": {
            "name": {"type": "string"}
        },
        "required": ["name"]
    }
    put = {
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"}
        },
        "required": ["id"],
    }
    delete = {
        "type": "object",
        "properties": {
            "id": {"type": "number"}
        },
        "required": ["id"]
    }

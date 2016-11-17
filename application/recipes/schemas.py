from marshmallow import Schema, fields, pre_load, post_dump

from ..recipes.models import *


class RecipeSchema(Schema):
    id = fields.Number()
    name = fields.String(required=True)
    description = fields.String()
    img_path = fields.String()
    categories = fields.List(fields.Int(), required=True)
    ingredients = fields.Dict(required=True)


class RecipeCategorySchema(Schema):
    id = fields.Int()
    name = fields.String(required=True)
    slug = fields.String()
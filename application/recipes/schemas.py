from marshmallow import Schema, fields, pre_load, post_dump

from ..recipes.models import *


class RecipeSchema_post(Schema):
    name = fields.String(required=True)
    description = fields.String()
    img_path = fields.String()
    categories = fields.List(fields.Int())
    ingredients = fields.Dict()


class RecipeSchema_put(Schema):
    id = fields.Int(required=True)
    name = fields.String()
    description = fields.String()
    img_path = fields.String()
    categories = fields.List(fields.Int())
    ingredients = fields.Dict()


class RecipeSchema_delete(Schema):
    id = fields.Int(required=True)


class RecipeCategorySchema(Schema):
    id = fields.Int()
    name = fields.String(required=True)
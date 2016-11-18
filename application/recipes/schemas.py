from marshmallow import Schema, fields


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


class RecipeCategorySchema_post(Schema):
    name = fields.String(required=True)


class RecipeCategorySchema_put(Schema):
    id = fields.Int(required=True)
    name = fields.String()


class RecipeCategorySchema_delete(Schema):
    id = fields.Int(required=True)
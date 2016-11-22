from marshmallow import Schema, fields


class IngredientSchema_post(Schema):
    name = fields.String(required=True)
    description = fields.String()
    img_path = fields.String()
    categories = fields.List(fields.Int())
    dimension = fields.String(required=True)


class IngredientSchema_put(Schema):
    id = fields.Int(required=True)
    name = fields.String()
    description = fields.String()
    img_path = fields.String()
    categories = fields.List(fields.Int())
    dimention = fields.String()


class IngredientSchema_delete(Schema):
    id = fields.Int(required=True)


class IngredientCategorySchema_post(Schema):
    name = fields.String(required=True)


class IngredientCategorySchema_put(Schema):
    id = fields.Int(required=True)
    name = fields.String()


class IngredientCategorySchema_delete(Schema):
    id = fields.Int(required=True)

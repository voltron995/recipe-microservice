from marshmallow import Schema, fields

from ..suppliers.schemas import SupplierSchema


class ProductSupplierSchema(Schema):
    price = fields.Int()
    supplier = fields.Nested(SupplierSchema)


class ProductSchema(Schema):
    id = fields.Int()
    name = fields.String()
    quantity = fields.Int()
    ingredient_id = fields.Int()
    suppliers = fields.Nested(
        ProductSupplierSchema, 
        attribute='suppliers_list', 
        many=True
    )
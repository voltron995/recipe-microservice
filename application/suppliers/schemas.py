from marshmallow import Schema, fields
from ..modelextention import * 


class SupplierSchema_post(Schema):
    name = fields.String(required=True)
    contact = fields.String(required = True)


class SupplierSchema_put(Schema):
    id = fields.Int(required=True)
    name = fields.String()
    contact = fields.String()


class SupplierSchema_delete(Schema):
    id = fields.Int(required=True)

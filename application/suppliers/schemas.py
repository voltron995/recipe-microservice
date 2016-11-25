from marshmallow import Schema, fields


class SupplierSchema(Schema):
    id = fields.Int()
    name = fields.String()
    contact = fields.String()
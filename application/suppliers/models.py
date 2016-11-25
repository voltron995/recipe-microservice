from ..modelextention import BaseModel, db


class Supplier(db.Model, BaseModel):
    __tablename__ = 'supplier'
    name = db.Column(db.String(50))
    contact = db.Column(db.Text())

    def __init__(self, name, contact):
        self.name = name
        self.contact = contact
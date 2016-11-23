from werkzeug.exceptions import BadRequest

from ..modelextention import *


class Supplier(db.Model, BaseModel):
    __tablename__ = 'supplier'
    name = db.Column(db.String(50))
    contact = db.Column(db.Text())



    def __init__(self, name, contact):
        self.name = name
        self.contact = contact
        self.slug = slugify(name)

from ..modelextention import ManyToManyClass, BaseModel, db
from ..suppliers.models import Supplier

class Product(db.Model, BaseModel):
    __tablename__= 'product'
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))
    # ingredient_backref = db.relationship("Ingredient", backref = "products")
    quantity = db.Column(db.Integer())
    suppliers = db.relationship('ProductSupplier',
                                    cascade="all,delete-orphan",
                                    backref=db.backref('product_backref', cascade='all'))

    def __init__(self, name, quantity, suppliers_list, ingredient_id):
        self.name = name
        self.quantity = quantity
        self.ingredient_id = ingredient_id
        self.suppliers_list = suppliers_list

    @property
    def suppliers_list(self):
        return self.suppliers

    @suppliers_list.setter
    def suppliers_list(self, value):
        self.gen_suppliers_list(value)

    def gen_suppliers_list(self, suppliers_list):
        """function that create ingredients from json data stored in dish_ingredients"""
        if suppliers_list:
            self.suppliers = []
            for supplier in suppliers_list:
                id_supplier = supplier['supplier']['id']
                price = supplier['price']
                assoc = ProductSupplier(price=price)
                assoc.supplier = Supplier.query.get(int(id_supplier))
                if assoc.supplier:
                    self.suppliers.append(assoc)
                else:
                    """if we have not ingredient with id id_ingredient than"""
                    raise BadRequest("Can't find ingredient with id {id}".format(id=id_supplier))


class ProductSupplier(db.Model, ManyToManyClass):
    __tablename__ = 'product_suplier'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='cascade'), primary_key=True)
    supplier_id = db.Column(
        db.Integer, 
        db.ForeignKey('supplier.id', ondelete='cascade'), 
        primary_key=True
    )
    price = db.Column(db.Integer)
    supplier = db.relationship(
        "Supplier", 
        backref='product_suplier_backref'
    )
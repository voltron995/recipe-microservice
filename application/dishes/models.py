from flask_sqlalchemy import event
from werkzeug.exceptions import BadRequest


from ..modelextention import *
from ..ingredients.models import Ingredient


class Dish(db.Model, BaseModel):
    __tablename__ = 'dish'
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text())
    img_path = db.Column(db.String(200))
    ingredients = db.relationship('DishIngredient',
                                    cascade="all,delete-orphan",
                                    backref=db.backref('dish_backref', cascade='all'))
    price = 0
    @property
    def ingredients_property(self):
        return self.ingredients

    @ingredients_property.setter
    def ingredients_property(self, value):
        self.gen_ingredients_list(value)

    def __init__(self, name, ingredients, description=None, img_path=None):
        self.name = name
        self.description = description
        self.img_path = img_path
        self.ingredients_property = ingredients
        self.slug = slugify(self.name)

    def gen_price(self):
        '''
        function which generate price for recipe
        '''
        self.price = 0
        price_ingr = []
        for assocc in self.ingredients:
            minimun_value=[]
            for product in assocc.ingredient.products:
                for supplier in product.suppliers:
                    minimun_value.append(supplier.price/product.quantity)
            price_ingr.append(int(assocc.quantity*min(minimun_value)))
        self.price = sum(price_ingr)
        self.price = "{:.2f}".format(self.price/100)


    def gen_ingredients_list(self, ingredients):
        """function that create ingredients from json data stored in dish_ingredients"""
        if ingredients:
            self.ingredients = []

            for id_ingredient, quantity in ingredients.items():
                assoc = DishIngredient(quantity=int(quantity))
                assoc.ingredients = Ingredient.query.get(int(id_ingredient))
                if assoc.ingredients:
                    self.ingredients.append(assoc)
                else:
                    """if we have not ingredient with id id_ingredient than"""
                    raise BadRequest("Can't find ingredient with id {id}".format(id=id_ingredient))
        self.gen_price()

    def get_attributes(self):
        attrs = super(Dish, self).get_attributes()
        self.gen_price()
        attrs.extend(['price'])
        return attrs

class DishIngredient(db.Model,ManyToManyClass):
    __tablename__ = 'dish_ingredient'
    dish_id = db.Column(db.Integer,
                        db.ForeignKey('dish.id', ondelete='cascade'),
                        primary_key=True)
    ingredient_id = db.Column(db.Integer,
                        db.ForeignKey('ingredient.id', ondelete='cascade'),
                        primary_key=True)
    quantity = db.Column(db.Integer)
    ingredients = db.relationship("Ingredient", backref='dish_ingredient_assocciation_backref')


@event.listens_for(Dish.ingredients, 'append')
@event.listens_for(Dish.ingredients, 'remove')
def dish_append_or_remove(target, value, initiator):
    # Update when a child is added or removed
    '''
    event handler, when updated recipe
    '''
    target.updated_timestamp = datetime.datetime.utcnow()

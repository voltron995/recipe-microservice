from flask_sqlalchemy import event
from werkzeug.exceptions import BadRequest


from ..modelextention import *
from ..ingredients.models import Ingredient, DishIngredient


class Dish(db.Model, BaseModel):
    __tablename__ = 'dish'

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text())
    image = db.Column(db.String(200))
    ingredients = db.relationship(
        'DishIngredient',
        cascade="all,delete-orphan",
        backref=db.backref('dish_backref', cascade='all')
    )

    @property
    def price(self):
        return self.gen_price()

    @property
    def ingredients_list(self):
        return self.ingredients

    @ingredients_list.setter
    def ingredients_list(self, value):
        self.gen_ingredients_list(value)

    def __init__(self, name, ingredients_list, description=None, image=None):
        self.name = name
        self.description = description
        self.image = image
        self.ingredients_list = ingredients_list

    def gen_price(self):
        price = 0
        price_ingr = []
        for assocc in self.ingredients:
            price_list=[]
            for product in assocc.ingredient.products:
                for supplier in product.suppliers:
                    price_list.append(supplier.price/product.quantity)
            if price_list:
                price_ingr.append(int(assocc.quantity * min(price_list)))
        if price_ingr:
            price = sum(price_ingr)
            return "{:.2f}".format(price/100)
        return "{:.2f}".format(0)


    def gen_ingredients_list(self, ingredients):
        """
        function that create ingredients from
        json data stored in dish_ingredients
        """
        if ingredients:
            self.ingredients = []
            for ingredient in ingredients:
                id_ingredient = ingredient['ingredient']['id']
                quantity = ingredient['quantity']
                assoc = DishIngredient(quantity=int(quantity))
                assoc.ingredient = Ingredient.query.get(id_ingredient)
                if assoc.ingredient:
                    self.ingredients.append(assoc)
                else:
                    """if we have not ingredient with id id_ingredient than"""
                    raise BadRequest("Can't find ingredient with id {id}".format(id=id_ingredient))

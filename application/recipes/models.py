from werkzeug.exceptions import BadRequest

from flask_sqlalchemy import event

from ..modelextention import *
from ..ingredients.models import Ingredient, RecipeIngredient


class Recipe(db.Model, BaseModel):
    __tablename__= 'recipe'

    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text())
    img_path = db.Column(db.String(200))
    categories = db.relationship(
        'RecipeCategory',
        secondary=create_table('recipe', 'recipe_category'),
        backref='recipe_backref'
    )
    ingredients = db.relationship(
        'RecipeIngredient',
        cascade="all,delete-orphan",
        backref=db.backref('recipe_backref', cascade='all')
    )

    @property
    def price(self):
        return self.get_price()

    @property
    def ingredients_list(self):
        return self.ingredients

    @ingredients_list.setter
    def ingredients_list(self, value):
        self.gen_ingredients_list(value)

    @property
    def categories_list(self):
        return self.categories

    @categories_list.setter
    def categories_list(self, value):
        self.gen_categories_list(value)

    def __init__(self, name, ingredients_list, categories=None, description=None, img_path=None):
        self.name = name
        self.description = description
        self.img_path = img_path
        self.ingredients_list = ingredients_list
        self.categories_list = categories

    def get_price(self):
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
        """function that create ingredients from json data stored in dish_ingredients"""
        if ingredients:
            self.ingredients = []
            for ingredient in ingredients:
                id_ingredient = ingredient['ingredient']['id']
                quantity = ingredient['quantity']
                assoc = RecipeIngredient(quantity=int(quantity))
                assoc.ingredient = Ingredient.query.get(id_ingredient)
                if assoc.ingredient:
                    self.ingredients.append(assoc)
                else:
                    """if we have not ingredient with id id_ingredient than"""
                    raise BadRequest("Can't find ingredient with id {id}".format(id=id_ingredient))

    def gen_categories_list(self, categories):
        if categories:
            self.categories = []
            for category in categories:
                id_category = category['id']
                category = RecipeCategory.query.get(id_category)
                if category:
                    self.categories.append(category)
                else:
                    """if we have not category with id id_category than"""
                    raise BadRequest("Can't find category with id {id}".format(id=id_category))

    def get_attributes(self):
        attrs = super(Recipe, self).get_attributes()
        self.gen_price()
        attrs.extend(['price'])
        return attrs


class RecipeCategory(db.Model, BaseModel):
    __tablename__ = 'recipe_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    slug = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name
        self.slug = slugify(self.name)
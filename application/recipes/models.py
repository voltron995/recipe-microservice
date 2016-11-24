from werkzeug.exceptions import BadRequest

from flask_sqlalchemy import event

from ..modelextention import *
from ..ingredients.models import Ingredient


class Recipe(db.Model, BaseModel):
    __tablename__= 'recipe'

    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text())
    img_path = db.Column(db.String(200))
    categories = db.relationship('RecipeCategory',
                                    secondary=create_table('recipe', 'recipe_category'),
                                    backref='recipe_backref')
    ingredients = db.relationship('RecipeIngredient',
                                    cascade="all,delete-orphan",
                                    backref=db.backref('recipe_backref', cascade='all'))
    price = 0

    @property
    def ingredients_property(self):
        return self.ingredients

    @ingredients_property.setter
    def ingredients_property(self, value):
        self.gen_ingredients_list(value)

    @property
    def categories_property(self):
        return self.categories

    @categories_property.setter
    def categories_property(self, value):
        self.gen_categories_list(value)

    def __init__(self, name, ingredients=None, categories=None, description=None, img_path=None):
        self.name = name
        self.description = description
        self.img_path = img_path
        self.slug = slugify(self.name)
        self.ingredients_property = ingredients
        self.categories_property = categories

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
                assoc = RecipeIngredient(quantity=int(quantity))
                assoc.ingredient = Ingredient.query.get(int(id_ingredient))
                if assoc.ingredient:
                    self.ingredients.append(assoc)
                else:
                    """if we have not ingredient with id id_ingredient than"""
                    raise BadRequest("Can't find ingredient with id {id}".format(id=id_ingredient))

    def gen_categories_list(self, categories):
        if categories:
            self.categories = []
            for id_category in categories:
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


class RecipeIngredient(db.Model, ManyToManyClass):
    __tablename__ = 'recipe_ingredient'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', ondelete='cascade'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id', ondelete='cascade'), primary_key=True)
    quantity = db.Column(db.Integer)
    ingredient = db.relationship("Ingredient", backref='recipe_ingredient_assocciation_backref')


class RecipeCategory(db.Model, BaseModel):
    __tablename__ = 'recipe_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    slug = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name
        self.slug = slugify(self.name)



@event.listens_for(Recipe.ingredients, 'append')
@event.listens_for(Recipe.ingredients, 'remove')
def receive_append_or_remove(target, value, initiator):
    # Update when a child is added or removed
    '''
    event handler, when updated recipe
    '''
    target.updated_timestamp = datetime.datetime.utcnow()

from ..modelextention import *
from ..ingredients.models import Ingredient
from werkzeug.exceptions import BadRequest


class Dish(db.Model, BaseModel):
    __tablename__ = 'dish'
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text())
    img_path = db.Column(db.String(200))
    ingredients = db.relationship('DishIngredient',
                                    cascade="all,delete-orphan",
                                    backref=db.backref('dish_backref', cascade='all'))

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

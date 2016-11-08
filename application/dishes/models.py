from ..modelextention import *
from ..ingredient.models import Ingredient


class Dish(db.Model, DateMixin):
    __tablename__ = 'dish'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text())
    img_path = db.Column(db.String(200))
    dish_ingredients = db.relationship('DishIngredient', backref="dish")

    def __init__(self, name, dish_ingredients, description=None, img_path=None):
    	self.name = name
    	self.description = description
    	self.img_path = img_path
    	self.gen_ingredients_list(dish_ingredients)
    	self.slug = slugify(self.name)    	

    def gen_ingredients_list(self, dish_ingredients):
    	"""function that create ingredients from json data stored in dish_ingredients"""
    	self.dish_ingredients = []
    	for id_ingredient, quantity in dish_ingredients.items():
    		assoc = DishIngredient(quantity=int(quantity))
    		assoc.ingredient = Ingredient.query.get(int(id_ingredient))
    		if assoc.ingredient:
    			self.dish_ingredients.append(assoc)
    		else:
    			"if we have not ingredient with id id_ingredient than"
    			raise ValueError

class DishIngredient(db.Model):
    __tablename__ = 'dish_ingredient'
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    quantity = db.Column(db.Integer)
    ingredient = db.relationship("Ingredient", backref="dish_association")
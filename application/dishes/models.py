from ..modelextention import *
from ..ingredient.models import Ingredient


class Dish(db.Model,DateMixin):
    __tablename__ = 'dish'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text())
    img_path = db.Column(db.String(200))
    dish_ingredients = db.relationship('Ingredient',
                                        secondary=create_table('dish', 'ingredient', 'quantity'),
                                        backref=db.backref('dish', lazy='dynamic'))

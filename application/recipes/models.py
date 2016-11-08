from ..modelextention import *
from ..ingredient.models import Ingredient


class RecipeCategory(db.Model,DateMixin):
    __tablename__ = 'recipe_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    slug = db.Column(db.String(50), unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '<RecipeCategory {}>'.format(self.name)

class Recipe(db.Model,DateMixin):
    __tablename__= 'recipe'
    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text())
    img_path =  db.Column(db.String(200))
    slug = db.Column(db.String(50), unique=True)
    categories = db.relationship('RecipeCategory',
                                 secondary=create_table('recipe', 'recipe_category'),
                                 backref=db.backref('recipes', lazy='dynamic'))
    rec_ingredients=db.relationship('Ingredient',
                                     secondary=create_table('recipe', 'ingredient', 'quantity'),
                                     backref=db.backref('recipes', lazy='dynamic'))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '<Recipe {}>'.format(self.name)

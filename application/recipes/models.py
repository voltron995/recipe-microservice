from ..modelextention import *
from ..ingredients.models import Ingredient


class Recipe(db.Model,DateMixin):
    __tablename__= 'recipe'
    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text())
    img_path = db.Column(db.String(200))
    slug = db.Column(db.String(50), unique=True)
    categories = db.relationship('RecipeCategory',
                                    secondary=create_table('recipe', 'recipe_category'))
    ingredients = db.relationship('RecipeIngredient', 
                                    cascade="all,delete-orphan",
                                    backref=db.backref("recipe", cascade="all"))

    def __init__(self, name, ingredients, categories, description=None, img_path=None):
        self.name = name
        self.description = description
        self.img_path = img_path
        self.slug = slugify(self.name)
        self.gen_ingredients_list(ingredients)
        self.gen_categories_list(categories)        

    def __repr__(self):
        return '<Recipe {}>'.format(self.name)

    def gen_ingredients_list(self, ingredients):
        """function that create ingredients from json data stored in dish_ingredients"""
        self.ingredients = []
        for id_ingredient, quantity in ingredients.items():
            assoc = RecipeIngredient(quantity=int(quantity))
            assoc.ingredients = Ingredient.query.get(int(id_ingredient))
            if assoc.ingredients:
                self.ingredients.append(assoc)
            else:
                "if we have not ingredient with id id_ingredient than"
                raise ValueError

    def gen_categories_list(self, categories):
        self.categories = []
        for id_category in categories:
            category = RecipeCategory.query.get(id_category)
            if category:
                self.categories.append(category)
            else:
                "if we have not category with id id_category than"
                raise ValueError

    @classmethod
    def _attrs_list(cls):
        return [item for item in cls.__dict__ if not item.startswith('_')]


class RecipeIngredient(db.Model, ManyToManyClass):
    __tablename__ = 'recipe_ingredient'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', ondelete='cascade'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id', ondelete='cascade'), primary_key=True)
    quantity = db.Column(db.Integer)
    ingredients = db.relationship("Ingredient", backref="recipe_association")


class RecipeCategory(db.Model, DateMixin):
    __tablename__ = 'recipe_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    slug = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name
        self.slug = slugify(self.name)
    
    @classmethod
    def _attrs_list(cls):
        return [item for item in cls.__dict__ if not item.startswith('_')]

    def __repr__(self):
        return '<RecipeCategory {}>'.format(self.name)
from ..modelextention import *
from ..ingredient.models import Ingredient


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
    recipe_ingredients = db.relationship('RecipeIngredient', backref='recipe')

    def __init__(self, name, recipe_ingredients, recipe_categories, description=None, img_path=None):
        self.name = name
        self.description = description
        self.img_path = img_path
        self.gen_ingredients_list(recipe_ingredients)
        self.gen_categories_list(recipe_categories)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '<Recipe {}>'.format(self.name)

    def gen_ingredients_list(self, recipe_ingredients):
        """function that create ingredients from json data stored in dish_ingredients"""
        self.recipe_ingredients = []
        for id_ingredient, quantity in recipe_ingredients.items():
            assoc = RecipeIngredient(quantity=int(quantity))
            assoc.ingredient = Ingredient.query.get(int(id_ingredient))
            if assoc.ingredient:
                self.recipe_ingredients.append(assoc)
            else:
                "if we have not ingredient with id id_ingredient than"
                raise ValueError

    def gen_categories_list(self, recipe_categories):
        self.categories = []
        for id_category in recipe_categories:
            category = RecipeCategory.query.get(id_category)
            if category:
                self.categories.append(category)
            else:
                "if we have not category with id id_category than"
                raise ValueError


class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredient'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    quantity = db.Column(db.Integer)
    ingredient = db.relationship("Ingredient", backref="recipe_association")


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
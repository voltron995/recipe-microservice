from werkzeug.exceptions import BadRequest

from ..modelextention import *


class Ingredient(db.Model, BaseModel):
    __tablename__ = 'ingredient'
    name = db.Column(db.String(50))
    description = db.Column(db.Text())
    dimension = db.Column(db.Text())
    categories = db.relationship('Category',
                                   secondary=create_table('ingredient', 'ingredient_category'),
                                   backref='ingredient_backref')
    products = db.relationship("Product", backref="ingredient_backref")
    # add image path

    @property
    def categories_property(self):
        return self.categories

    @categories_property.setter
    def categories_property(self, value):
        self.gen_categories_list(value)

    def __init__(self, name, dimension, img_path=None, description=None, categories=None):
        self.name = name
        self.dimension = dimension
        self.description = description
        self.categories_property = categories

    def gen_categories_list(self, categories):
        if categories:
            self.categories = []
            for category in categories:
                id_category = category['id']
                category = Category.query.get(id_category)
                if category:
                    self.categories.append(category)
                else:
                    """if we have not category with id id_category than"""
                    raise BadRequest("Can't find category with id {id}".format(id=id_category))


class Category(db.Model, BaseModel):
    __tablename__ = 'ingredient_category'
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

class DishIngredient(db.Model, ManyToManyClass):
    __tablename__ = 'dish_ingredient'
    dish_id = db.Column(
        db.Integer,
        db.ForeignKey('dish.id', ondelete='cascade'),
        primary_key=True
    )
    ingredient_id = db.Column(
        db.Integer,
        db.ForeignKey('ingredient.id', ondelete='cascade'),
        primary_key=True)
    quantity = db.Column(db.Integer)
    ingredient = db.relationship(
        "Ingredient", 
        backref='dish_ingredient_assocciation_backref'
    )

class RecipeIngredient(db.Model, ManyToManyClass):
    __tablename__ = 'recipe_ingredient'
    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey('recipe.id', ondelete='cascade'), 
        primary_key=True
    )
    ingredient_id = db.Column(
        db.Integer, 
        db.ForeignKey(
            'ingredient.id', 
            ondelete='cascade'
        ),
        primary_key=True
    )
    quantity = db.Column(db.Integer)
    ingredient = db.relationship(
        "Ingredient", 
        backref='recipe_ingredient_assocciation_backref'
    )



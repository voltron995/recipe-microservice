from werkzeug.exceptions import BadRequest

from ..modelextention import *


class Ingredient(db.Model, BaseModel):
    __tablename__ = 'ingredient'
    name = db.Column(db.String(50))
    description = db.Column(db.Text())
    dimension = db.Column(db.Text())
    categories=db.relationship('IngredientCategory',
                                   secondary=create_table('ingredient', 'ingredient_category'),
                                   backref='ingredient_backref')
    products = db.relationship("Product", backref="ingredient_backref")

    @property
    def categories_property(self):
        return self.categories

    @categories_property.setter
    def categories_property(self, value):
        self.gen_categories_list(value)

    def __init__(self, name, dimension, description=None, categories=None):
        self.name = name
        self.slug = slugify(self.name)
        self.dimension = dimension
        self.description = description
        self.categories_property = categories


    def gen_categories_list(self, categories):
        if categories:
            self.categories = []
            for id_category in categories:
                category = IngredientCategory.query.get(id_category)
                if category:
                    self.categories.append(category)
                else:
                    """if we have not category with id id_category than"""
                    raise BadRequest("Can't find category with id {id}".format(id=id_category))


class IngredientCategory(db.Model, BaseModel):
    __tablename__ = 'ingredient_category'
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name
        self.slug = slugify(self.name)

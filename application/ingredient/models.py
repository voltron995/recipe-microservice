from ..modelextention import *

class Ingredient(db.Model,DateMixin):
    __tablename__ = 'ingredient'
    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text())
    dimension = db.Column(db.Text())
    in_categories= db.relationship('IngredientCategory',
                                   secondary=create_table('ingredient', 'ingredient_category'),
                                   backref=db.backref('ingredient', lazy='dynamic'))


class IngredientCategory(db.Model,DateMixin):
    __tablename__ = 'ingredient_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    slug = db.Column(db.String(50), unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug = slugify(self.name)

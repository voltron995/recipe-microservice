import datetime
import re
from .app import db


def slugify(s):
    return re.sub('[^\w]+', '-', s).lower()

recipe_recipe_category = db.Table('recipe_recipe_category',
    db.Column('recipe_category_id', db.Integer, db.ForeignKey('recipe_category.id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))
)

class Recipe(db.Model):
    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text())
    img_path =  db.Column(db.String(200))
    slug = db.Column(db.String(50), unique=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    categories = db.relationship('RecipeCategory',
                                 secondary=recipe_recipe_category,
                                 backref=db.backref('recipes', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '<Recipe {}>'.format(self.name)

class RecipeCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    slug = db.Column(db.String(50), unique=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '<RecipeCategory {}>'.format(self.name)

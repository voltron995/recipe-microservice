from flask import Blueprint
from .views import *


urls = [
    ('/<string:slug>', IngredientById,'IngredientEntity'),
    ('', IngredientView, 'Ingredient'),
    ('/categories', CategoryView, 'IngredientCategory')
]

ingredients = Blueprint('ingredients', __name__)

for url_str, view_class, endpoint_name in urls:
    ingredients.add_url_rule(url_str, view_func=view_class.as_view(endpoint_name))

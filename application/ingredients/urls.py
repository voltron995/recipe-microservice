from flask import Blueprint
from .views import *


urls = [
    ('/<int:ingredient_id>', IngredientById,'ingredient_entity'),
    ('', IngredientView, 'ingredient'),
    ('/categories', CategoryView, 'ingredient_categories')
]

ingredients = Blueprint('ingredients', __name__)

for url_str, view_class, endpoint_name in urls:
    ingredients.add_url_rule(url_str, view_func=view_class.as_view(endpoint_name))

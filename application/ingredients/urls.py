from flask import Blueprint
from .views import *


urls = [
    ('/<int:id>', IngredientEntity, 'IngredientEntity'),
    ('', IngredientList, 'IngredientList'),
    ('/categories', CategoryList, 'IngredientCategory'),
    ('/categories/<int:id>', CategoryEntity, 'IngredientCategoryEntity')
]

ingredients = Blueprint('ingredients', __name__)

for url_str, view_class, endpoint_name in urls:
    ingredients.add_url_rule(url_str, view_func=view_class.as_view(endpoint_name))

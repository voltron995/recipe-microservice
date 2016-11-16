from flask import Blueprint
from .views import *


urls = [
    ('/<string:rcp_slug>/', RecipeBySlug, 'recipe_entity'),
    ('/', RecipeView, 'recipe'),
    ('/categories/', CategoryView, 'recipe_categories')
]

recipes = Blueprint('recipes', __name__)

for url_str, view_class, endpoint_name in urls:
    recipes.add_url_rule(url_str, view_func=view_class.as_view(endpoint_name))

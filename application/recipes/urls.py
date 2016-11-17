from flask import Blueprint,request
from .views import *
from .schemas import *
urls = [
    ('/<string:rcp_slug>/', RecipeBySlug, 'recipe_entity' ),
    ('/', RecipeView, 'recipe_api'),
    ('/categories/', CategoryView, 'recipe_categories_api' )
]

recipes = Blueprint('recipes', __name__)

for url_str, view_class, endpoint_name in urls:
    recipes.add_url_rule(url_str, view_func=view_class.as_view(endpoint_name))

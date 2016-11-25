from flask import Blueprint
from .views import *


urls = [
    ('/categories', CategoryList, 'RecipeCategory'),
    ('/categories/<int:id>', CategoryEntity, 'RecipeCategoryEntity'),    
    ('/<int:id>', RecipeEntity, 'RecipeEntity'),
    ('', RecipeList, 'RecipeList')
]

recipes = Blueprint('recipes', __name__)

for url_str, view_class, endpoint_name in urls:
    recipes.add_url_rule(url_str, view_func=view_class.as_view(endpoint_name))
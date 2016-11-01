from flask import Blueprint
from .views import *


urls = [
    ('/', Categories, 'category_list'),
    ('/<int:ctgr_id>/', CategoryById, 'category_entity'),
    ('/<int:ctgr_id>/recipes/', RecipesOfCategory, 'recipe_list_of_category'),
]

categories = Blueprint('categories', __name__)

for url_str, view_class, endpoint_name in urls:
    categories.add_url_rule(url_str, view_func=view_class.as_view(endpoint_name))

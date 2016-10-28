from .app import app
from .views import *


urls = [
    ('/', ApiList, 'api_list'),
    ('/categories/', Categories, 'categories_list'),
    ('/categories/<int:ctgr_id>/', CategoryById, 'category_entity'),
    ('/categories/<int:ctgr_id>/recipes/', CategoryRecipes, 'category_recipes_list'),
    ('/recipes/<int:rcp_id>/', RecipeById, 'recipe_entity'),
]

for url_str, view_class, endpoint_name in urls:
    app.add_url_rule(url_str, view_func=view_class.as_view(endpoint_name))

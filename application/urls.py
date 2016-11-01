from .app import app
from .actions.urls import actions
from .categories.urls import categories
from .recipes.urls import recipes


app.register_blueprint(actions, url_prefix='/actions')
app.register_blueprint(categories, url_prefix='/categories')
app.register_blueprint(recipes, url_prefix='/recipes')

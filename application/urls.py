from .app import app
from .actions.urls import actions
from .recipes.urls import recipes
from .dishes.urls import dishes
from .ingredients.urls import ingredients


app.register_blueprint(actions, url_prefix='/actions')
app.register_blueprint(recipes, url_prefix='/recipes')
app.register_blueprint(dishes, url_prefix='/dishes')
app.register_blueprint(ingredients, url_prefix='/ingredients')
from .app import app
from .actions.urls import actions
from .recipes.urls import recipes
from .dishes.urls import dishes
from .ingredients.urls import ingredients
from .products.urls import products
from .suppliers.urls import suppliers

app.register_blueprint(actions, url_prefix='/actions')
app.register_blueprint(recipes, url_prefix='/recipes')
app.register_blueprint(dishes, url_prefix='/dishes')
app.register_blueprint(ingredients, url_prefix='/ingredients')
app.register_blueprint(products, url_prefix='/products')
app.register_blueprint(suppliers, url_prefix='/suppliers')

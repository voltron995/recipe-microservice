from flask.views import MethodView
from werkzeug.exceptions import NotFound

from ..facilities import json_response, BaseApiView
from .models import Ingredient, IngredientCategory
from .schemas import *


class IngredientById(MethodView):    
    def get(self, slug):
        ingredient = Ingredient.query.filter_by(slug=slug)
        if ingredient:
            return json_response(ingredient)
        raise NotFound


class IngredientView(BaseApiView):
    _model = Ingredient
    _schema_post = IngredientSchema_post
    _schema_put = IngredientSchema_put
    _schema_delete = IngredientSchema_delete


class CategoryView(BaseApiView):
    _model = IngredientCategory
    _schema_post = IngredientCategorySchema_post
    _schema_put = IngredientCategorySchema_put
    _schema_delete = IngredientCategorySchema_delete
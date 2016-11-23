from flask.views import MethodView
from werkzeug.exceptions import NotFound

from ..facilities import json_response, BaseApiView, BaseApiEntityView
from .models import Ingredient, IngredientCategory
from .schemas import *


class IngredientById(BaseApiEntityView):
    _model = Ingredient
    _schema_put = IngredientSchema_put
    _schema_delete = IngredientSchema_delete


class IngredientView(BaseApiView):
    _model = Ingredient
    _schema_post = IngredientSchema_post


class CategoryById(BaseApiEntityView):
    _model = IngredientCategory
    _schema_put = IngredientCategorySchema_put
    _schema_delete = IngredientCategorySchema_delete


class CategoryView(BaseApiView):
    _model = IngredientCategory
    _schema_post = IngredientCategorySchema_post

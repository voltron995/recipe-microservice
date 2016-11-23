from flask.views import MethodView
from werkzeug.exceptions import NotFound

from ..facilities import json_response, BaseApiView, BaseApiEntityView
from ..valid_json import Validator
from .models import Recipe, RecipeCategory
from .schemas import *
from ..app import db


class RecipeById(BaseApiEntityView):
    _model = Recipe
    _schema_put = RecipeSchema_put
    _schema_delete = RecipeSchema_delete


class RecipeView(BaseApiView):
    _model = Recipe
    _schema_post = RecipeSchema_post


class CategoryById(BaseApiEntityView):
    _model = RecipeCategory
    _schema_put = RecipeCategorySchema_put
    _schema_delete = RecipeCategorySchema_delete
    

class CategoryView(BaseApiView):
    _model = RecipeCategory
    _schema_post = RecipeCategorySchema_post
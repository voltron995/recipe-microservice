from flask.views import MethodView
from werkzeug.exceptions import NotFound

from ..facilities import json_response, BaseApiView
from .models import Recipe, RecipeCategory
from .schemas import *


class RecipeBySlug(MethodView):
    def get(self, slug):
        recipe = Recipe.query.filter_by(slug=slug).first()
        if recipe: 
            return json_response(recipe)
        raise NotFound


class RecipeView(BaseApiView):
    _model = Recipe
    _schema_post = RecipeSchema_post
    _schema_put = RecipeSchema_put
    _schema_delete = RecipeSchema_delete


class CategoryView(BaseApiView):
    _model = RecipeCategory
    _schema_post = RecipeCategorySchema_post
    _schema_put = RecipeCategorySchema_put
    _schema_delete = RecipeCategorySchema_delete
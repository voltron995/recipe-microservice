from flask import request
from sqlalchemy.sql import and_, or_

from ..facilities import ListCreate, RetrieveUpdateDelete
from .models import Recipe, RecipeCategory
from ..ingredients.models import RecipeIngredient
from .schemas import RecipeSchema, CategorySchema


class RecipeList(ListCreate):
    _model = Recipe
    _schema = RecipeSchema

    def get_objects_list(self):
        data = request.args
        recipes = Recipe.query.filter()
        if 'ingredients' in data:
            recipes = self.filter_ingredients(recipes, data['ingredients'])
        if 'categories' in data:
            recipes = self.filter_category(recipes, data['categories'])
        return recipes.all()

    def filter_category(self, recipes, categories):
        categories = [int(category) for category in categories.split(',')]
        recipes = recipes.filter(Recipe.categories.any(RecipeCategory.id.in_(categories)))
        return recipes

    def filter_ingredients(self, recipes, ingredients):
        ingredients = [int(ingredient) for ingredient in ingredients.split(',')]
        for ingredient in ingredients:
            recipes = recipes.filter(Recipe.ingredients.any(ingredient_id=ingredient))
        return recipes


class RecipeEntity(RetrieveUpdateDelete):
    _model = Recipe
    _schema = RecipeSchema


class CategoryList(ListCreate):
    _model = RecipeCategory
    _schema = CategorySchema


class CategoryEntity(RetrieveUpdateDelete):
    _model = RecipeCategory
    _schema = CategorySchema
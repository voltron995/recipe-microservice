from ..facilities import ListCreate, RetrieveUpdateDelete
from .models import Recipe, RecipeCategory
from .schemas import RecipeSchema, CategorySchema


class RecipeList(ListCreate):
    _model = Recipe
    _schema = RecipeSchema


class RecipeEntity(RetrieveUpdateDelete):
    _model = Recipe
    _schema = RecipeSchema


class CategoryList(ListCreate):
    _model = RecipeCategory
    _schema = CategorySchema


class CategoryEntity(RetrieveUpdateDelete):
    _model = RecipeCategory
    _schema = CategorySchema
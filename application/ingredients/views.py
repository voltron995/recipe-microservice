from ..facilities import ListCreate, RetrieveUpdateDelete
from .models import Ingredient, Category
from .schemas import *


class IngredientEntity(RetrieveUpdateDelete):
    _model = Ingredient
    _schema = IngredientSchema


class IngredientList(ListCreate):
    _model = Ingredient
    _schema = IngredientSchema


class CategoryEntity(RetrieveUpdateDelete):
    _model = Category
    _schema = CategorySchema


class CategoryList(ListCreate):
    _model = Category
    _schema = CategorySchema
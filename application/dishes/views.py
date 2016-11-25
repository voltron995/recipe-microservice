from ..facilities import ListCreate, RetrieveUpdateDelete
from .models import Dish
from .schemas import DishSchema


class DishEntity(RetrieveUpdateDelete):
    _model = Dish
    _schema = DishSchema


class DishList(ListCreate):
    _model = Dish
    _schema = DishSchema

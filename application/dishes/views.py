from flask.views import MethodView
from werkzeug.exceptions import NotFound

from ..facilities import json_response, BaseApiView, BaseApiEntityView
from .models import Dish
from .schemas import *


class DishById(BaseApiEntityView):
    _model = Dish
    _schema_put = DishSchema_put
    _schema_delete = DishSchema_delete


class DishView(BaseApiView):
    _model = Dish
    _schema_post = DishSchema_post

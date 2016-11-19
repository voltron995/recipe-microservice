from flask.views import MethodView
from werkzeug.exceptions import NotFound

from ..facilities import json_response, BaseApiView
from .models import Dish
from .schemas import *


class DishById(MethodView):
    def get(self, dish_id):
        """Returns JSON response with a Dish entity of the given ID"""
        r = Dish.query.filter_by(id=dish_id).first()
        if r:
            return json_response(r)
        return json_response(code=404, msg='bad recipe in url')


class DishView(BaseApiView):
    _model = Dish
    _schema_post = DishSchema_post
    _schema_put = DishSchema_put
    _schema_delete = DishSchema_delete
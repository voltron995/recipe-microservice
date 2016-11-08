import json
from collections import OrderedDict
from flask import request
from flask.views import MethodView
from sqlalchemy.exc import DataError
from ..app import app, db
from ..dishes.models import Dish
from ..facilities import json_response

class DishById(MethodView):
    def get(self, dish_id):
        """Returns JSON response with a Recipe entity of the given ID"""
        r = Dish.query.get(dish_id)
        print("fdff")
        return json_response(r)

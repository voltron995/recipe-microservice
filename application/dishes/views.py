import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
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
        return json_response(r)

class DishSchema:
    post = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            'description': {'type': "string"},
            "img_path": {"type": "string"},
            "dish_ingredients": {"type": "object"}
        },
        "required": ["name", "dish_ingredients"],
    }

class DishView(MethodView):
    def post(self):
        if json_validate(request.json, DishSchema.post):
            dish_json = request.json
            dish = Dish(name=dish_json.get("name"), 
                dish_ingredients=dish_json.get("dish_ingredients"),
                description=dish_json.get("description", ""), 
                img_path=dish_json.get("img_path", ""))
            db.session.add(dish)
            db.session.commit()
            return json.dumps({"correct": "200"})
        return json.dumps({"error": "403"})


def json_validate(json, schema):
    print(request)
    try:
        validate(json, schema)
    except ValidationError:
        return False
    else:
        return True


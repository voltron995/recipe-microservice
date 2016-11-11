import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from collections import OrderedDict
from flask import request
from flask.views import MethodView
from sqlalchemy.exc import DataError


from ..app import app, db
from ..dishes.models import Dish
from ..facilities import json_response, json_validate


class DishById(MethodView):
    def get(self, dish_id):
        """Returns JSON response with a Dish entity of the given ID"""
        r = Dish.query.filter_by(id=dish_id).first()
        if r:
            return json_response(r)
        return json_response(code=404, msg='bad recipe in url')

class DishSchema:
    post = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            'description': {'type': "string"},
            "img_path": {"type": "string"},
            "ingredients": {"type": "object"}
        },
        "required": ["name", "ingredients"],
    }
    put = {
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "img_path": {"type": "string"},
            "ingredients": {"type": "object"},

        },
        "required": ["id"],
    }
    delete = {
        "type": "object",
        "properties": {
            "id": {"type": "number"}
        },
        "required": ["id"]
    }


class DishView(MethodView):
    def get(self):
        dishes = Dish.query.filter()
        for arg in request.args:
            if arg not in Dish._attrs_list():
                return json_response(code=403, msg='bad argument in request')
        if 'id' in request.args:
            dishes = dishes.filter_by(id=request.args['id'])
        if 'name' in request.args:
            dishes = dishes.filter_by(name=request.args['name'])
        if 'description' in request.args:
            dishes = dishes.filter_by(description=request.args['description'])
        if 'ingrefients' in request.args:
            for ingredient in request.args['ingredients'].split(','):
                dishes = dishes.filter(Dish.ingredients.any(id=ingredient))
        return json_response(dishes.all())

    def post(self):
        if json_validate(request.json,DishSchema.post):
            dish_json = request.json
            dish = Dish(name=dish_json.get("name"),
                ingredients=dish_json.get("ingredients"),
                description=dish_json.get("description", ""),
                img_path=dish_json.get("img_path", ""))
            db.session.add(dish)
            db.session.commit()
            return json_response(dish)
        return json.dumps({"error": "403"})

    def put(self):
        if json_validate(request.json, DishSchema.put):
            dish_json = request.json
            dish = Dish.query.get(dish_json["id"])
            if dish:
                dish.name = dish_json.get("name") or dish.name
                dish.description = dish_json.get("description") or dish.description
                dish.img_path = dish_json.get("img_path") or dish.img_path
                if "ingredients" in dish_json:
                    dish.gen_ingredients_list(dish_json["ingredients"])
                db.session.commit()
                return json_response(dish)
            else:
                return json_response()
        return json_response()

    def delete(self):
        if json_validate(request.json, DishSchema.delete):
            dish_json = request.json
            dish= Dish.query.get(dish_json["id"])
            if dish:
                db.session.delete(dish)
                db.session.commit()
                return json_response({"OK": 200})
            else:
                return json_response()
        else:
            return json_response()

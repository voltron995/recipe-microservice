import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from collections import OrderedDict
from flask import request
from flask.views import MethodView
from sqlalchemy.exc import DataError
from ..app import app, db
from ..ingredients.models import Ingredient, IngredientCategory
from ..facilities import json_response


ERROR = json.dumps({"ERROR": 400})
OK = json.dumps({"OK": 200})

class IngredientById(MethodView):
    
    def get(self, ingredient_id):
        """Returns JSON response with a Ingredient entity of the given ID"""
        requested_ingredient = Ingredient.query.get(ingredient_id)
        return json_response(requested_ingredient)

class IngredientView(MethodView):

    def post(self):
        if validate_json_schema(request.json, IngredientSchema.post):
            ingredient_data = request.json
            ingredient = Ingredient(id=ingredient_data.get("id"),
                                    name=ingredient_data.get("name"),
                                    description=ingredient_data.get('description', ""),
                                    dimension=ingredient_data.get("dimension"),
                                    in_categories=ingredient_data.get("in_categories"))
            db.session.add(ingredient)
            db.session.commit()
            return json_response(ingredient)        
        raise Exception('Bad json schema in dish')

    def put(self):
        if validate_json_schema(request.json, IngredientSchema.put):
            ingredient_data = request.json
            old_ingredient = Ingredient.query.get(ingredient_data["id"])
            old_ingredient.name = ingredient_data.get("name") or old_ingredient.name
            old_ingredient.description = ingredient_data.get("description") or old_ingredient.description
            old_ingredient.dimension = ingredient_data.get("dimension") or old_ingredient.dimension
            print(ingredient_data)
            if "in_categories" in ingredient_data:
                old_ingredient.in_categories = ingredient_data.get("in_categories") or old_ingredient.in_categories 

            db.session.commit()
            return json_response(old_ingredient)
        return Exception('Bad json schema in dish')

    def delete(self):

        if validate_json_schema(request.json, IngredientSchema.delete):
            ingredient_data = request.json
            ingredient_to_delete = Ingredient.query.get(ingredient_data["id"])
            if ingredient_to_delete:
                db.session.delete(ingredient_to_delete)
                db.session.commit()
                return OK
        return Exception('Bad json schema in dish')

class CategoryView(MethodView):
    def get(self):
        categories = IngredientCategory.query.filter()
        for arg in request.args:
            if arg not in RecipeCategory._attrs_list():
                return ERROR
        if 'id' in request.args:
            categories = categories.filter_by(id=request.args['id'])
        if 'name' in request.args:
            categories = categories.filter_by(name=request.args['name'])
        return json_response(categories.all())

    def post(self):
        if validate_json_schema(request.json, CategorySchema.post):
            category_json = request.json
            category = IngredientCategory(name=category_json.get("name"))
            db.session.add(category)
            db.session.commit()
            return json_response(category)
        return ERROR

    def put(self):
        if validate_json_schema(request.json, CategorySchema.put):
            category_json = request.json
            category = IngredientCategory.query.get(category_json["id"])
            if category:
                category.name = category_json.get("name") or category.name
                db.session.commit()
                return json_response(category)
        return ERROR

    def delete(self):
        if validate_json_schema(request.json, CategorySchema.delete):
            category_json = request.json
            category = IngredientCategory.query.get(category_json["id"])
            if category:
                db.session.delete(category)
                db.session.commit()
                return OK
        return ERROR

class IngredientSchema:

    post = {
        "type":"object",
        "properties": {
            "id":{"type":"number"},
            "name":{"type":"string"},
            "description":{"type":"string"},
            "dimension":{"type":"string"},
            "in_categories":{"type":"array", "items":{"type":"number"}}},
        "required":["id", "name", "dimension", "in_categories"]
    }

    put = {
        "type":"object",
        "properties": {
            "id":{"type":"number"},
            "name":{"type":"string"},
            "description":{"type":"string"},
            "dimension":{"type":"string"},
            "in_categories":{"type":"array", "items":{"type":"number"}}},
        "required":["id"]
    }

    delete = {
        "type":"object",
        "properties":{
            "id":{"type":"number"}
        },
        "required":["id"]
    }

class CategorySchema:
    post = {
        "type": "object",
        "properties": {
            "name": {"type": "string"}
        },
        "required": ["name"]
    }
    
    put = {
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"}
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

def validate_json_schema(json, schema):
    try:
        validate(json, schema)
    except ValidationError:
        return False
    else:
        return True
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from collections import OrderedDict
from flask import request
from flask.views import MethodView
from sqlalchemy.exc import DataError

from ..app import app, db
from .models import Recipe, RecipeCategory
from ..facilities import json_response


class RecipeById(MethodView):
    def get(self, rcp_id):
        """Returns JSON response with a Recipe entity of the given ID"""
        r = Recipe.query.get(rcp_id)
        return json_response(r)


class RecipeSchema:
    post = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            'description': {'type': "string"},
            "img_path": {"type": "string"},
            "recipe_ingredients": {"type": "object"},
            "recipe_categories": {"type": "array"}
        },
        "required": ["name", "recipe_ingredients", "recipe_categories"],
    }
    put = {
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "img_path": {"type": "string"},
            "recipe_ingredients": {"type": "object"},
            "recipe_categories": {"type": "array"}
        },
        "required": ["id"],
    }


class RecipeView(MethodView):
    def post(self):
        if json_validate(request.json, RecipeSchema.post):
            recipe_json = request.json
            recipe = Recipe(name=recipe_json.get("name"), 
                recipe_ingredients=recipe_json.get("recipe_ingredients"),
                recipe_categories=recipe_json.get("recipe_categories"),
                description=recipe_json.get("description", ""), 
                img_path=recipe_json.get("img_path", ""))
            db.session.add(recipe)
            db.session.commit()
            return json.dumps({"correct": "200"})
        return json.dumps({"error": "403"})

    def put(self):
    	print(request.json)
    	validate(request.json, RecipeSchema.put)
    	if json_validate(request.json, RecipeSchema.put):
    		recipe_json = request.json
    		recipe = Recipe.query.get(recipe_json["id"])
    		recipe.name = recipe_json.get("name") or recipe.name
    		recipe.description = recipe_json.get("description") or recipe.description
    		recipe.img_path = recipe_json.get("img_path") or recipe.img_path
    		if "recipe_ingredients" in recipe_json:
    			recipe.gen_ingredients_list(recipe_json["recipe_ingredients"])
    		if "recipe_categories" in recipe_json:
    			recipe.gen_categories_list(recipe_json["recipe_categories"])
    		db.session.commit()
    		return "+++"
    	return "None"


def json_validate(json, schema):
    print(request)
    try:
        validate(json, schema)
    except ValidationError:
        return False
    else:
        return True
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


class IngredientById(MethodView):
    
    def get(self, ingredient_id):
        """Returns JSON response with a Ingredient entity of the given ID"""
        requested_ingredient = Ingredient.query.get(ingredient_id)
        return json_response(requested_ingredient)

    def post(self):

    	if validate_json_schema(request.json, IngredientSchema.post):
    		ingredient_data = request.json
    		ingredient = Ingredient(name=ingredient_data.get("name"),
    								description=ingredient_data.get('description', ""),
    								dimension=ingredient_data.get("dimension"),
    								in_categories=ingredient_data.get("in_categories"))
   			db.session.add(ingredient)
   			db.session.commit()
   			return self.get(ingredient['id'])
   		return json.dumps({"error":" 400"})

   	def put(self):

   		if validate_json_schema(request.json, IngredientSchema.put):
   			ingredient_data = request.json
   			old_ingredient = self.get(ingredient_data["id"])
   			old_ingredient.name = ingredient_data.get("name") or old_ingredient.name
   			old_ingredient.description = ingredient_data.get("description") or old_ingredient.description
   			old_ingredient.dimension = ingredient_data.get("dimension") or old_ingredient.dimension
   			if "in_categories" in ingredient_data:
   				IngredientCategory.query.filter(IngredientCategory.)





class IngredientSchema:
	properties = {"properties": {
			"id":{"type":"number"},
			"name":{"type":"string"},
			"description":{"type":"string"},
			"dimension":{"type":"string"},
			"in_categories":{"type":"string"}}
		}

	post = {
		"type":"object",
		properties,
		"required":["name", "dimension", "in_categories"],
	}

	put = {
		"type":"object",
		properties,
		"required":["id"]
	}

def validate_json_schema(json, schema):
	try:
		validate(json, schema)
	except ValidationError:
		return False
	else:
		return True
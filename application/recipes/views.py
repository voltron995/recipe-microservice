import json
from collections import OrderedDict
from flask import request
from flask.views import MethodView
from sqlalchemy.exc import DataError

from ..app import app, db
from .models import Recipe, RecipeCategory
from ..facilities import json_response, json_validate


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
            "ingredients": {"type": "object"},
            "categories": {"type": "array"}
        },
        "required": ["name", "ingredients", "categories"],
    }
    put = {
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "img_path": {"type": "string"},
            "ingredients": {"type": "object"},
            "categories": {"type": "array"}
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


class RecipeView(MethodView):
    def post(self):
        if json_validate(request.json, RecipeSchema.post):
            recipe_json = request.json
            recipe = Recipe(name=recipe_json.get("name"), 
                ingredients=recipe_json.get("ingredients"),
                categories=recipe_json.get("categories"),
                description=recipe_json.get("description", ""), 
                img_path=recipe_json.get("img_path", ""))
            db.session.add(recipe)
            db.session.commit()
            return json_response(recipe)
        return json.dumps({"error": "403"})

    def put(self):
        if json_validate(request.json, RecipeSchema.put):
            recipe_json = request.json
            recipe = Recipe.query.get(recipe_json["id"])
            if recipe:
                recipe.name = recipe_json.get("name") or recipe.name
                recipe.description = recipe_json.get("description") or recipe.description
                recipe.img_path = recipe_json.get("img_path") or recipe.img_path
                if "ingredients" in recipe_json:
                    recipe.gen_ingredients_list(recipe_json["ingredients"])
                if "categories" in recipe_json:
                    recipe.gen_categories_list(recipe_json["categories"])
                db.session.commit()
                return json_response(recipe)
            else:
                return json_response()
        return json_response()

    def delete(self):
        if json_validate(request.json, RecipeSchema.delete):
            recipe_json = request.json
            recipe = Recipe.query.get(recipe_json["id"])
            if recipe:
                db.session.delete(recipe)
                db.session.commit()
                return json_response({"OK": 200})
            else:
                return json_response()
        else:
            return json_response()



import json
from flask import request, jsonify, Flask
from flask.views import MethodView
from werkzeug.exceptions import BadRequest, NotFound


from ..err_handler import *
from ..app import app, db
from .models import Recipe, RecipeCategory
from ..facilities import json_response, json_validate
from .schemas import *
from ..valid_json import Validator


class RecipeBySlug(MethodView):
    def get(self, rcp_slug):
        """Returns JSON response with a Recipe entity of the given ID"""
        r = Recipe.query.filter_by(slug=rcp_slug).first()
        if r:
            return json_response(r)
        raise NotFound('Bad recipe in url')


class RecipeView(MethodView):
    def get(self):
        recipes = self.filter()
        return json_response(recipes.all())

    def post(self):
        data = Validator().validate_schema(Recipe.get_schema())["data"]
        recipe = Recipe(name=data["name"],
                ingredients=data["ingredients"],
                categories=data["categories"],
                description=data["description"],
                img_path=data["img_path"])
        db.session.add(recipe)
        db.session.commit()
        result = Recipe.query.get(recipe.id)
        return json_response(result)

    def put(self):
        data = Validator().validate_schema(Recipe.get_schema())["data"]
        recipe = Recipe.query.get(data["id"])
        if recipe:
            recipe.name = data["name"] or recipe.name
            recipe.description = data["description"] or recipe.description
            recipe.img_path = data["img_path"] or recipe.img_path
            if "ingredients" in data:
                recipe.gen_ingredients_list(data["ingredients"])
            if "categories" in data:
                recipe.gen_categories_list(data["categories"])
            db.session.commit()
            return json_response(recipe)
        else:
            raise BadRequest('Can not found recipe with id {}'.format(int(data["id"])))

    def delete(self):
        data = Validator().validate_schema(Recipe.get_schema())["data"]
        recipe = Recipe.query.get(data["id"])
        if recipe:
            db.session.delete(recipe)
            db.session.commit()
            return json_response({"OK": 200})
        else:
            raise BadRequest('Can not found recipe with id {}'.format(int(data["id"])))

    @staticmethod
    def filter():
        recipes = Recipe.query.filter()
        for arg in request.args:
            if arg not in Recipe._attrs_list():
                raise BadRequest('wrong argument {arg} in request'.format(arg=arg))
        if 'id' in request.args:
            recipes = recipes.filter_by(id=request.args['id'])
        if 'name' in request.args:
            recipes = recipes.filter_by(name=request.args['name'])
        if 'description' in request.args:
            recipes = recipes.filter_by(description=request.args['description'])
        if 'categories' in request.args:
            for category in request.args['categories'].split(','):
                recipes = recipes.filter(Recipe.categories.any(id=category))
        if 'ingredients' in request.args:
            for ingredient in request.args['ingredients'].split(','):
                recipes = recipes.filter(Recipe.ingredients.any(id=ingredient))
        return recipes


class CategoryView(MethodView):
    def get(self):
        categories = self.filter()
        return json_response(categories.all())

    def post(self):
        data = Validator().validate_schema(Recipe.get_schema())["data"]
        category = RecipeCategory(name=data["name"])
        db.session.add(category)
        db.session.commit()
        return json_response(category)

    def put(self):
        data = Validator().validate_schema(Recipe.get_schema())["data"]
        category = RecipeCategory.query.get(data["id"])
        if category:
            category.name = category_json.get("name") or category.name
            db.session.commit()
            return json_response(category)
        else:
            raise BadRequest('Can not found category with id {}'.format(int(data["id"])))

    def delete(self):
        data = Validator().validate_schema(Recipe.get_schema())["data"]
        category = RecipeCategory.query.get(data["id"])
        if category:
            db.session.delete(category)
            db.session.commit()
            return json_response({'OK': 200})
        else:
            raise BadRequest('Can not found category with id {}'.format(int(data["id"])))

    @staticmethod
    def filter():
        categories = RecipeCategory.query.filter()
        for arg in request.args:
            if arg not in RecipeCategory._attrs_list():
                raise BadRequest('wrong argument {arg} in request'.format(arg=arg))
        if 'id' in request.args:
            categories = categories.filter_by(id=request.args['id'])
        if 'name' in request.args:
            categories = categories.filter_by(name=request.args['name'])
        return categories
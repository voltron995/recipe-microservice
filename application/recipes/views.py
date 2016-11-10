import json
from collections import OrderedDict
from flask import request
from flask.views import MethodView
from sqlalchemy.exc import DataError

from ..app import app, db
from .models import Recipe, RecipeCategory
from ..facilities import json_response, json_validate
from .schemas import *


class RecipeBySlug(MethodView):
    def get(self, rcp_slug):
        """Returns JSON response with a Recipe entity of the given ID"""
        r = Recipe.query.filter_by(slug=rcp_slug).first()
        if r:
            return json_response(r)
        return json_response(code=404, msg='bad recipe in url')


class RecipeView(MethodView):
    def get(self):
        recipes = Recipe.query.filter()
        for arg in request.args:
            if arg not in Recipe._attrs_list():
                return json_response(code=403, msg='bad argument in request')
        if 'id' in request.args:
            recipes = recipes.filter_by(id=request.args['id'])
        if 'name' in request.args:
            recipes = recipes.filter_by(name=request.args['name'])
        if 'description' in request.args:
            recipes = recipes.filter_by(description=request.args['description'])
        if 'categories' in request.args:
            for category in request.args['categories'].split(','):
                recipes = recipes.filter(Recipe.categories.any(id=category))
        if 'ingrefients' in request.args:
            for ingredient in request.args['ingredients'].split(','):
                recipes = recipes.filter(Recipe.ingredients.any(id=ingredient))
        return json_response(recipes.all())

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
        return json_response(code=403, msg='validation error')

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
                return json_response(code=404, msg='cannot found recipe with id {}'.format(recipe_json["id"]))
        return json_response(code=403, msg='validation error')

    def delete(self):
        if json_validate(request.json, RecipeSchema.delete):
            recipe_json = request.json
            recipe = Recipe.query.get(recipe_json["id"])
            if recipe:
                db.session.delete(recipe)
                db.session.commit()
                return json_response({"OK": 200})
            else:
                return json_response(code=404, msg='cannot found recipe with id {}'.format(recipe_json["id"]))
        else:
            return json_response(code=403, msg='validation error')


class CategoryView(MethodView):
    def get(self):
        categories = RecipeCategory.query.filter()
        for arg in request.args:
            if arg not in RecipeCategory._attrs_list():
                return json_response(code=403, msg='bad argument in request')
        if 'id' in request.args:
            categories = categories.filter_by(id=request.args['id'])
        if 'name' in request.args:
            categories = categories.filter_by(name=request.args['name'])
        return json_response(categories.all())

    def post(self):
        if json_validate(request.json, CategorySchema.post):
            category_json = request.json
            category = RecipeCategory(name=category_json.get("name"))
            db.session.add(category)
            db.session.commit()
            return json_response(category)
        return json_response(code=403, msg='validation error')

    def put(self):
        if json_validate(request.json, CategorySchema.put):
            category_json = request.json
            category = RecipeCategory.query.get(category_json["id"])
            if category:
                category.name = category_json.get("name") or category.name
                db.session.commit()
                return json_response(category)
            else:
                return json_response(code=404, msg='cannot found recipe with id {}'.format(category_json["id"]))
        return json_response(code=403, msg='validation error')

    def delete(self):
        if json_validate(request.json, CategorySchema.delete):
            category_json = request.json
            category = RecipeCategory.query.get(category_json["id"])
            if category:
                db.session.delete(category)
                db.session.commit()
                return json_response({'OK': 200})
            else:
                return json_response(code=404, msg='cannot found recipe with id {}'.format(category_json["id"]))
        return json_response(code=403, msg='validation error')
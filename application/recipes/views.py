import json
from flask import request, jsonify, Flask
from flask.views import MethodView


from ..err_handler import *
from ..app import app, db
from .models import Recipe, RecipeCategory
from ..facilities import json_response, json_validate
from .schemas import *
from ..valid_json import *

class RecipeBySlug(MethodView):
    def get(self, rcp_slug):
        """Returns JSON response with a Recipe entity of the given ID"""
        r = Recipe.query.filter_by(slug=rcp_slug).first()
        if r:
            return json_response(r)
        return json_response(code=404, msg='bad recipe in url')

#@app.errorhandler(Exception)
#def er_hand(exception):
#    return json_response(str(exception))

class RecipeView(MethodView,Valid_json):
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
        data = self.validate_schema(RecipeSchema)
        if "errors" in data:
             return(json_response(data))
        data = data["data"]
        recipe = Recipe(name=data["name"],
                ingredients=data["ingredients"],
                categories=data["categories"],
                description=data["description"],
                img_path=data["img_path"])
        db.session.add(recipe)
        db.session.commit()
        result = Recipe.query.get(recipe.id)
        return json_response(result,code=200,msg='recipe created successfully')

    def put(self):
        data = self.validate_schema(RecipeSchema)
        if "errors" in data:
             return(json_response(data))
        data = data["data"]
        recipe = Recipe.query.get(data["id"])
        if data["id"]:
            return json_response(code=404, msg='cannot found recipe with id {}'.format(data["id"]))
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

    def delete(self):
        data = self.validate_schema(RecipeSchema)
        if "errors" in data:
             return(json_response(data))
        data = data["data"]
        recipe = Recipe.query.get(data["id"])
        if recipe:
            db.session.delete(recipe)
            db.session.commit()
            return json_response({"OK": 200})
        else:
            return json_response(code=404, msg='cannot found recipe with id {}'.format(data["id"]))


class CategoryView(MethodView,Valid_json):
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
        data = self.validate_schema(RecipeCategorySchema)
        if "errors" in data:
             return(json_response(data))
        data = data["data"]
        category = RecipeCategory(name=data["name"])
        db.session.add(category)
        db.session.commit()
        return json_response(category)

    def put(self):
        data = self.validate_schema(RecipeCategorySchema)
        if "errors" in data:
             return(json_response(data))
        data = data["data"]
        category = RecipeCategory.query.get(data["id"])
        if category:
            category.name = category_json.get("name") or category.name
            db.session.commit()
            return json_response(category)
        else:
            return json_response(code=404, msg='cannot found recipe with id {}'.format(category_json["id"]))
        return json_response(code=403, msg='validation error')

    def delete(self):
        data = self.validate_schema(RecipeCategorySchema)
        if "errors" in data:
             return(json_response(data))
        data = data["data"]
        category = RecipeCategory.query.get(data["id"])
        if category:
            db.session.delete(category)
            db.session.commit()
            return json_response({'OK': 200})
        else:
            return json_response(code=404, msg='cannot found recipe with id {}'.format(category_json["id"]))
        return json_response(code=403, msg='validation error')

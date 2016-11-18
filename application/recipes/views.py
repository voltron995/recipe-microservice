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


class BaseApiView(MethodView):
    def filter(self, data):
        model_objects = self._model.query.filter()
        fields = self._model.__mapper__.columns.keys()
        fields_relation = self._model.__mapper__.relationships.keys()

        for attr in fields:
            if attr in data:
                model_objects = model_objects.filter(getattr(self._model, attr)==data[attr])
        for attr in fields_relation:
            if attr in data:
                for attr_id in data[attr].split(','):
                    model_objects = model_objects.filter(getattr(self._model, attr).any(id=attr_id))
        return model_objects.all()

    def create(self, data):
        model_object = self._model(**data)
        db.session.add(model_object)
        db.session.commit()
        created_object = self._model.query.get(model_object.id)
        return created_object

    def update(self, data):
        model_object = self._model.query.get(data['id'])
        if model_object:
            fields = self._model.__mapper__.columns.keys()
            fields_relation = self._model.__mapper__.relationships.keys()
            for attr in fields:
                if attr in data:
                    setattr(model_object, attr, data[attr])
            for attr in fields_relation: 
                if attr in data:
                    setattr(model_object, attr+'_property', data[attr])
            db.session.commit()
            return model_object
        else:
            raise BadRequest('Can not found {} with id {}'.format(self._model.__tablename__, data["id"])) 

    def remove(self, data):
        model_object = self._model.query.get(data["id"])
        if model_object:
            db.session.delete(model_object)
            db.session.commit()
            return 200, 'Successfully deleted {} with id {}'.format(self._model.__tablename__, data["id"])
        else:
            raise BadRequest('Can not found {} with id {}'.format(self._model.__tablename__, data["id"]))


class RecipeView(BaseApiView):
    _model = Recipe

    def get(self):
        recipes = self.filter(request.args)
        return json_response(recipes)

    def post(self):
        data = Validator().validate_schema(RecipeSchema_post)
        recipe = self.create(data)
        return json_response(recipe)

    def put(self):
        data = Validator().validate_schema(RecipeSchema_put)
        recipe = self.update(data)
        return json_response(recipe)

    def delete(self):
        data = Validator().validate_schema(RecipeSchema_delete)
        code, msg = self.remove(data)
        return json_response(code=code, msg=msg)


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
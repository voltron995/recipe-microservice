import json
from collections import OrderedDict
from flask import request
from flask.views import MethodView
from sqlalchemy.exc import DataError
from ..app import app, db
from ..models import Recipe, RecipeCategory
from ..facilities import json_response


class Categories(MethodView):
    def get(self):
        """Returns JSON response with a list of Categories"""
        rcp_ctgrs = [OrderedDict([('id', c.id), ('name', c.name)]) for c in RecipeCategory.query.all()]
        return json_response(rcp_ctgrs)

    def post(self):
        """Creates new Category in the DB and returns JSON response with it."""
        j = json.loads(request.data.decode())

        if len(j) != 1 or not j.get('name', None) or not j['name']:
            return json_response(None)

        rc = RecipeCategory(**j)
        try:
            db.session.add(rc)
            db.session.commit()
        except DataError as e:
            return json_response({"error": e.args})

        return json_response(rc)

class CategoryById(MethodView):
    def get(self, ctgr_id):
        """Returns JSON response with a Category entity of the given ID"""
        c = RecipeCategory.query.get(ctgr_id)
        return json_response(c)

class RecipesOfCategory(MethodView):
    def get(self, ctgr_id):
        """Returns JSON response with a list of Recipes for the given Category ID"""
        ctgr_rcps = [OrderedDict([('id', r.id), ('name', r.name)]) for r in RecipeCategory.query.get(ctgr_id).recipes]
        return json_response(ctgr_rcps)

from collections import OrderedDict
from flask.views import MethodView
from .app import app
from .models import Recipe, RecipeCategory
from .facilities import json_response


class ApiList(MethodView):
    def get(self):
        """Returns JSON response with a list of available API URLs"""
        rule_dict = OrderedDict()
        for rule in app.url_map.iter_rules():
            if rule.endpoint in ('api_list', 'static'):
                continue
            rule_dict[rule.rule] = list(rule.methods)
        return json_response(rule_dict)

class Categories(MethodView):
    def get(self):
        """Returns JSON response with a list of Categories"""
        rcp_ctgrs = [OrderedDict([('id', c.id), ('name', c.name)]) for c in RecipeCategory.query.all()]
        return json_response(rcp_ctgrs)

class CategoryById(MethodView):
    def get(self, ctgr_id):
        """Returns JSON response with a Category entity of the given ID"""
        c = RecipeCategory.query.get(ctgr_id)
        return json_response(c)

class CategoryRecipes(MethodView):
    def get(self, ctgr_id):
        """Returns JSON response with a list of Recipes for the given Category ID"""
        ctgr_rcps = [OrderedDict([('id', r.id), ('name', r.name)]) for r in RecipeCategory.query.get(ctgr_id).recipes]
        return json_response(ctgr_rcps)

class RecipeById(MethodView):
    def get(self, rcp_id):
        """Returns JSON response with a Recipe entity of the given ID"""
        r = Recipe.query.get(rcp_id)
        return json_response(r)

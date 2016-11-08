from collections import OrderedDict
from flask.views import MethodView
from ..app import app
from .models import Recipe, RecipeCategory
from ..facilities import json_response


class RecipeById(MethodView):
    def get(self, rcp_id):
        """Returns JSON response with a Recipe entity of the given ID"""
        r = Recipe.query.get(rcp_id)
        return json_response(r)

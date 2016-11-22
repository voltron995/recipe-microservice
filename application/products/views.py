from flask.views import MethodView
from werkzeug.exceptions import NotFound

from ..facilities import json_response, BaseApiView
from .models import Product
from .schemas import *


class ProductBySlug(MethodView):
    def get(self, slug):
        product = Product.query.filter_by(slug=slug)
        if product:
            return json_response(product)
        raise NotFound


class ProductView(BaseApiView):
    _model = Product
    _schema_post = ProductSchema_post
    _schema_put = ProductSchema_put
    _schema_delete = ProductSchema_delete

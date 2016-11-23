from flask.views import MethodView
from werkzeug.exceptions import NotFound

from ..facilities import json_response, BaseApiView, BaseApiEntityView
from .models import Product
from .schemas import *


class ProductBySlug(BaseApiEntityView):
    _model = Product
    _schema_put = ProductSchema_put
    _schema_delete = ProductSchema_delete


class ProductView(BaseApiView):
    _model = Product
    _schema_post = ProductSchema_post
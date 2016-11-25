from flask.views import MethodView
from werkzeug.exceptions import NotFound

from ..facilities import ListCreate, RetrieveUpdateDelete

from .models import Product
from .schemas import ProductSchema


class ProductEntity(RetrieveUpdateDelete):
    _model = Product
    _schema = ProductSchema


class ProductList(ListCreate):
    _model = Product
    _schema = ProductSchema
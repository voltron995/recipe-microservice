from flask.views import MethodView
from werkzeug.exceptions import NotFound

from ..facilities import json_response, BaseApiView
from .models import Supplier
from .schemas import *


class SupplierBySlug(MethodView):
    def get(self, slug):
        supplier = Supplier.query.filter_by(slug=slug)
        if supplier:
            return json_response(supplier)
        raise NotFound


class SupplierView(BaseApiView):
    _model = Supplier
    _schema_post = SupplierSchema_post
    _schema_put = SupplierSchema_put
    _schema_delete = SupplierSchema_delete

from flask.views import MethodView
from werkzeug.exceptions import NotFound

from ..facilities import json_response, BaseApiView, BaseApiEntityView
from .models import Supplier
from .schemas import *


class SupplierById(BaseApiEntityView):
    _model = Supplier
    _schema_put = SupplierSchema_put
    _schema_delete = SupplierSchema_delete


class SupplierView(BaseApiView):
    _model = Supplier
    _schema_post = SupplierSchema_post
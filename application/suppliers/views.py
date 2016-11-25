from ..facilities import ListCreate, RetrieveUpdateDelete
from .models import Supplier
from .schemas import *


class SupplierEntity(RetrieveUpdateDelete):
    _model = Supplier
    _schema = SupplierSchema


class SupplierList(ListCreate):
    _model = Supplier
    _schema = SupplierSchema
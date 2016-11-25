from flask import Blueprint
from .views import *


urls = [
    ('/<int:id>', SupplierEntity,'SupplierEntity'),
    ('', SupplierList, 'SupplierList')
]

suppliers = Blueprint('suppliers', __name__)

for url_str, view_class, endpoint_name in urls:
    suppliers.add_url_rule(url_str, view_func=view_class.as_view(endpoint_name))

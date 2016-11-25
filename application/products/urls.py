from flask import Blueprint
from .views import *


urls = [
    ('/<int:id>', ProductEntity,'ProductEntity'),
    ('', ProductList, 'ProductList')
]

products = Blueprint('products', __name__)

for url_str, view_class, endpoint_name in urls:
    products.add_url_rule(url_str, view_func=view_class.as_view(endpoint_name))

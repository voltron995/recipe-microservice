from flask import Blueprint
from .views import *


urls = [
    ('/<string:slug>', ProductBySlug,'ProductEntity'),
    ('', ProductView, 'Product')
]

products = Blueprint('products', __name__)

for url_str, view_class, endpoint_name in urls:
    products.add_url_rule(url_str, view_func=view_class.as_view(endpoint_name))

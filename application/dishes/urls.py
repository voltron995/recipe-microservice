from flask import Blueprint
from .views import *


urls = [
   ('/<string:slug>', DishById, 'DishEntity'),
   ('', DishView, 'Dish')]

dishes = Blueprint('dishes', __name__)

for url_str, view_class, endpoint_name in urls:
	dishes.add_url_rule(url_str, view_func=view_class.as_view(endpoint_name))
from flask import Blueprint
from .views import *


urls = [
   ('/<int:dish_id>/', DishById, 'dish_entity'),
   ('/', DishView, 'dish_api')]

dishes = Blueprint('dishes', __name__)
for url_str, view_class, endpoint_name in urls:
	dishes.add_url_rule(url_str, view_func=view_class.as_view(endpoint_name))
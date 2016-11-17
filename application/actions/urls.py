from flask import Blueprint
from .views import *


urls = [
    ('', ActionList, 'action_urls'),
    ('/<action_name>', ActionName, 'action_url')
]

actions = Blueprint('actions', __name__)

for url_str, view_class, endpoint_name in urls:
    actions.add_url_rule(url_str, view_func=view_class.as_view(endpoint_name))

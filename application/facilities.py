import json
from collections import OrderedDict
from datetime import datetime
from flask import make_response
from flask_sqlalchemy import Model
from sqlalchemy.orm.dynamic import Query


def model_serializer(model_obj):
    """
    Returns OrderedDict with attributes of a given SQLAlchemy model instance
    with suitable datetime values.
    """
    fields = model_obj.__mapper__.columns.keys()
    fields.extend(model_obj.__mapper__.relationships.keys())
    valid_dict = OrderedDict()

    for field in fields:
        val = getattr(model_obj, field)
        if isinstance(val, datetime):
            val = val.isoformat()
        elif isinstance(val, Query):
            val = [obj.id for obj in val.all()]
        elif isinstance(val, list):
            val = [obj.id for obj in val]
        valid_dict[field] = val

    return valid_dict

def json_response(arg):
    """
    Returns valid JSON response.
    """
    if arg is None:
        arg = {"error":"404"}
    elif isinstance(arg, Model):
        arg = model_serializer(arg)

    response = make_response(json.dumps(arg, indent=4))
    response.headers['Content-type'] = "application/json"

    return response

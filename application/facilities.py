import json
from collections import OrderedDict
from datetime import datetime
from flask import make_response, abort
from flask_sqlalchemy import Model
from sqlalchemy.orm.dynamic import Query
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from .modelextention import ManyToManyClass

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
            value = val.isoformat()
        elif isinstance(val, Query):
            value = [obj.id for obj in val.all()]
        elif isinstance(val, list):
            value = []
            for obj in val:
                if isinstance(obj, ManyToManyClass):
                    attrs = obj.__mapper__.columns.keys()
                    attrs =  [item for item in attrs if not item.endswith('_id')]
                    table = getattr(obj, field)
                    table_fields = getattr(obj, field).__mapper__.columns.keys()
                    val_dict = {}
                    for f in table_fields:
                        val_dict[f] = getattr(table, f)
                    for f in attrs:
                        val_dict[f] = getattr(obj, f)
                    value.append(val_dict)
                else:
                    table_fields = obj.__mapper__.columns.keys()
                    val_dict = {}
                    for f in table_fields:
                        val_dict[f] = getattr(obj, f)
                    value.append(val_dict)
        else:
            value = val
        valid_dict[field] = value
    return valid_dict
def json_response(args=None, code=200, msg=''):
    """
    Returns valid JSON response.
    """
    if args is None:
        arg = {"error": {'message': msg}}
    elif isinstance(args, Model):
        arg = model_serializer(args)
    elif isinstance(args, list):
        arg = []
        for model in args:
            arg.append(model_serializer(model))
    else:
        arg = args
    response = make_response(json.dumps(arg, indent=4))
    response.headers['Content-type'] = "application/json"
    return response, code
def json_validate(json, schema):
    try:
        validate(json, schema)
    except ValidationError:
        return False
    else:
        return True

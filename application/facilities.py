import json
from collections import OrderedDict
from datetime import datetime
from flask import make_response, request
from flask.views import MethodView
from flask_sqlalchemy import Model
from sqlalchemy.orm.dynamic import Query
from werkzeug.exceptions import BadRequest

from .app import db
from .modelextention import ManyToManyClass
from .valid_json import Validator

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
                    table_fields = {item for item in getattr(obj, field).__mapper__.columns.keys()}
                    table_fields -= {'created_timestamp', 'updated_timestamp'}
                    val_dict = {}
                    for f in table_fields:
                        val_dict[f] = getattr(table, f)
                    for f in attrs:
                        val_dict[f] = getattr(obj, f)
                    value.append(val_dict)
                else:
                    table_fields = {item for item in obj.__mapper__.columns.keys()}
                    table_fields -= {'created_timestamp', 'updated_timestamp'}
                    val_dict = {}
                    for f in table_fields:
                        val_dict[f] = getattr(obj, f)
                    value.append(val_dict)
        else:
            value = val
        valid_dict[field] = value
    json_response = {}
    json_response["id"] = valid_dict["id"]
    json_response["type"] = model_obj.__tablename__
    json_response["attributes"] = {key: value for key, value in valid_dict.items() if key != 'id'}
    return json_response

def json_response(args=None, code=200, msg=''):
    """
    Returns valid JSON response.
    """
    if isinstance(args, Model):
        arg = {}
        arg["data"] = model_serializer(args)
    elif isinstance(args, list):
        arg = {}
        arg["data"] = []
        for model in args:
            arg["data"].append(model_serializer(model))
    else:
        arg = {'message': msg}
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


class BaseApiView(MethodView):

    def get(self):
        recipes = self.filter(request.args)
        return json_response(recipes)

    def post(self):
        data = Validator().validate_schema(self._schema_post)
        recipe = self.create(data)
        return json_response(recipe)

    def put(self):
        data = Validator().validate_schema(self._schema_put)
        recipe = self.update(data)
        return json_response(recipe)

    def delete(self):
        data = Validator().validate_schema(self._schema_delete)
        code, msg = self.remove(data)
        return json_response(code=code, msg=msg)


    def filter(self, data):
        model_objects = self._model.query.filter()
        fields = self._model.__mapper__.columns.keys()
        fields_relation = self._model.__mapper__.relationships.keys()
        for attr in fields:
            if attr in data:
                model_objects = model_objects.filter(getattr(self._model, attr)==data[attr])
        for attr in fields_relation:
            if attr in data:
                for attr_id in data[attr].split(','):
                    model_objects = model_objects.filter(getattr(self._model, attr).any(id=attr_id))
        return model_objects.all()

    def create(self, data):
        model_object = self._model(**data)
        db.session.add(model_object)
        db.session.commit()
        created_object = self._model.query.get(model_object.id)
        return created_object

    def update(self, data):
        model_object = self._model.query.get(data['id'])
        if model_object:
            fields = self._model.__mapper__.columns.keys()
            fields_relation = self._model.__mapper__.relationships.keys()
            for attr in fields:
                if attr in data:
                    setattr(model_object, attr, data[attr])
            for attr in fields_relation: 
                if attr in data:
                    setattr(model_object, attr+'_property', data[attr])
            db.session.commit()
            return model_object
        else:
            raise BadRequest('Can not found {} with id {}'.format(self._model.__tablename__, data["id"])) 

    def remove(self, data):
        model_object = self._model.query.get(data["id"])
        if model_object:
            db.session.delete(model_object)
            db.session.commit()
            return 200, 'Successfully deleted {} with id {}'.format(self._model.__tablename__, data["id"])
        else:
            raise BadRequest('Can not found {} with id {}'.format(self._model.__tablename__, data["id"]))

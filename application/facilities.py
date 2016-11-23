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


def json_specification(json_data, model):
    json_response = OrderedDict()
    json_response["id"] = json_data["id"]
    json_response["type"] = model.__tablename__
    json_response["attributes"] = {key: value for key, value in json_data.items() if key != 'id'}
    return json_response

def model_serializer(model):
    attributes = model.get_attributes()
    json_dict = OrderedDict()
    for attr in attributes:
        json_dict[attr] = attr_to_json(getattr(model, attr))
    return json_specification(json_dict, model)
    # return json_dict

def attr_to_json(attr):
    if isinstance(attr, datetime):
            value = attr.isoformat()
    elif isinstance(attr, list):
        value = []
        for obj in attr:
            obj_dict = attr_to_json(obj)
            value.append(obj_dict)
    elif isinstance(attr, Model):
        if isinstance(attr, ManyToManyClass):
            obj_dict = OrderedDict()
            for row in attr.get_attributes():
                mtm_attr = getattr(attr, row)
                if isinstance(mtm_attr, Model):
                    for cell in mtm_attr.get_attributes():
                        obj_dict[cell] = attr_to_json(getattr(mtm_attr, cell))
                else:
                    obj_dict[row] = attr_to_json(getattr(attr, row))                
            value = json_specification(obj_dict, attr)
        else:
            value = model_serializer(attr)
    else:
        value = attr
    return value

def json_response(args=None, code=200, msg=''):
    if isinstance(args, Model):
        arg = {}
        arg["data"] = model_serializer(args)
    elif isinstance(args, list):
        arg = {}
        arg["data"] = []
        for model in args:
            obj = model_serializer(model)
            arg["data"].append(obj)
    else:
        arg = args
    response = make_response(json.dumps(arg, indent=4))
    response.headers['Content-type'] = "application/json"
    return response, code
    
class BaseApiEntityView(MethodView):
    def get(self, id):
        obj = self._model.query.filter_by(id=id).first()
        if obj: 
            return json_response(obj)
        raise NotFound

    def put(self, id):
        data = Validator().validate_schema(self._schema_put)
        model_object = self.update(data)
        return json_response(model_object)

    def delete(self, id):
        data = Validator().validate_schema(self._schema_delete)
        code, msg = self.remove(data)
        return json_response(code=code, msg=msg)

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


class BaseApiView(MethodView):

    def get(self):
        model_objects = self.filter(request.args)
        return json_response(model_objects)

    def post(self):
        data = Validator().validate_schema(self._schema_post)
        model_object = self.create(data)
        return json_response(model_object)

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
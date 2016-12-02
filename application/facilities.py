import json
from collections import OrderedDict
from datetime import datetime
from flask import make_response, request
from flask.views import MethodView
from flask_sqlalchemy import Model
from sqlalchemy.orm.dynamic import Query
from werkzeug.exceptions import BadRequest, NotFound
from marshmallow import Schema, fields, pre_load, validate
from marshmallow.exceptions import ValidationError

from .recipes.models import Recipe
from .app import db, logger
from .modelextention import ManyToManyClass
from .valid_json import Validator


def make_json_response(attrs=None, code=200):
    response = make_response(json.dumps(attrs, indent=4))
    response.headers['Content-type'] = "application/json"
    return response, code


class ValidationMaxin:
    def validate_schema(self, json=None, schema=None):
        if json is None:
            raise BadRequest("Can't find json file in request body")
        data, errors = schema().load(json)
        if errors:
            logger.error(errors)
        return data, errors


class ListCreate(MethodView, ValidationMaxin):
    _model = None
    _schema = None

    def get_objects_list(self):
        return self._model.query.filter().all()

    def get(self):
        object_list = self.get_objects_list()
        objects_json = self._schema(many=True).dump(object_list).data
        return make_json_response(objects_json)

    def post(self):
        data, errors = self.validate_schema(
            request.get_json(silent=True),
            self._schema
        )
        if errors:
            return make_json_response(errors, 400)
        valid_name = self._model.query.filter_by(name=data['name']).first
        if valid_name:
            raise ValidationError('Name: Duplicated value')
        return data
        new_object = self._model(**data)
        db.session.add(new_object)
        db.session.commit()
        new_object = self._schema().dump(new_object).data
        logger.info("Created {0}".format(new_object))
        return make_json_response(new_object, 201)


class RetrieveUpdateDelete(MethodView, ValidationMaxin):
    _schema = None
    _model = None

    def get_object(self, id):
        obj = self._model.query.get(id)
        if obj:
            return obj
        raise NotFound('Can not found {} with id {}'.format(
            self._model.__tablename__,
            id
        ))

    def get(self, id):
        obj = self.get_object(id)
        obj_json = self._schema().dump(obj).data
        return make_json_response(obj_json)

    def update(self, id, data):
        model_object = self._model.query.get(id)
        if model_object:
            fields = self._model.__mapper__.columns.keys()
            fields_relation = self._model.__mapper__.relationships.keys()
            for attr in fields:
                if attr in data:
                    setattr(model_object, attr, data[attr])
            for attr in fields_relation:
                if attr+'_list' in data:
                    setattr(model_object, attr+'_list', data[attr+'_list'])
            db.session.commit()
            return model_object
        raise NotFound('Can not found {} with id {}'.format(
            self._model.__tablename__,
            id
        ))

    def put(self, id):
        data, errors = self.validate_schema(
            request.get_json(silent=True),
            self._schema
        )
        if errors:
            return make_json_response(errors, 400)
        obj = self.update(id, data)
        obj_json = self._schema().dump(obj).data
        logger.info("Updated {0}".format(obj_json))
        return make_json_response(obj_json, 200)

    def delete(self, id):
        obj = self._model.query.get(id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            logger.info("Deleted{0}".format(obj))
            return make_json_response({}, code=200)
        raise NotFound('Can not found {} with id {}'.format(
            self._model.__tablename__,
            id
        ))

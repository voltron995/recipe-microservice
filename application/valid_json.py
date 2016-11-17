from marshmallow import Schema, fields, pre_load, post_dump
from flask import request,jsonify


class Valid_json():
    def __init__(self):
        self._json = request.get_json()
    def validate_schema(self, schema):
        if not self._json:
            return json_response(msg='No input data provided',code=400)
        data, errors = schema().load(self._json)
        resp = {}
        if errors:
            resp["errors"] = errors
            return resp
        resp["data"] = data
        return resp

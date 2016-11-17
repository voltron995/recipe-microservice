from marshmallow import Schema, fields, pre_load, post_dump
from flask import request, jsonify


class Valid_json():
    def __init__(self):
        print(request.__dict__)
        self._json = self.get_json_or_None()          

    @staticmethod
    def get_json_or_None():
        if request.__dict__['environ']['CONTENT_TYPE'] == 'application/json':
            if request.__dict__['environ']['CONTENT_LENGTH']:
                return request.json

    def validate_schema(self, schema):
        if self._json is None:
            raise Exception("Can't find json file")
        data, errors = schema().load(self._json)
        resp = {}
        if errors:
            raise Exception(errors)
        resp["data"] = data
        return resp
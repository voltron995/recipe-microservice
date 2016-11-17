from flask import request, jsonify


class Validator:
    def __init__(self):
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
        if errors:
            raise Exception(errors)
        response_json = {}
        response_json["data"] = data
        return response_json
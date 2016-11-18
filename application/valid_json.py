from flask import request, jsonify
from werkzeug.exceptions import BadRequest


class Validator:
    def __init__(self):
        self._json = self.get_json_or_None()

    @staticmethod
    def get_json_or_None():
        try:
            return request.json
        except BadRequest:
            return None

    def validate_schema(self, schema):
        if self._json is None:
            raise BadRequest("Can't find json file in request body")
        data, errors = schema().load(self._json)
        if errors:
            raise BadRequest(errors)
        return data
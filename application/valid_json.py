from flask import request, jsonify
from werkzeug.exceptions import BadRequest

from .app import logger

class Validator:
    def __init__(self):
        self._json = request.get_json(silent=True)

    def validate_schema(self, schema):
        if self._json is None:
            raise BadRequest("Can't find json file in request body")
        data, errors = schema().load(self._json)
        if errors:
            logger.error(errors)
            raise BadRequest(errors)
        return data

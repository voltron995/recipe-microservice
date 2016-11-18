from flask import logging, jsonify
from .app import *
from werkzeug.exceptions import default_exceptions as http_exceptions
from werkzeug.exceptions import HTTPException

from .facilities import json_response


@app.errorhandler(Exception)
def handle_error(e):
    """
    handle exception and return json responce
    """
    code = 500
    name = 'Server Error'
    description = str(e)
    error_details = [{"code": code, "name": name, "description": description}]
    return jsonify({'errors': error_details}), code


def handle_http_error(e):
    error_details = []
    if isinstance(e.description, dict):        
        for key, value in e.description.items():
            error_details.append({"code": e.code, "name": e.name, "description": key + ": " + value[0]})
    else:
        error_details.append({"code": e.code, "name": e.name, "description": e.description})
    return jsonify({'errors': error_details}), e.code


# Register http exceptions to error handler
for code in http_exceptions:
    app.register_error_handler(code, handle_http_error)
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
    if isinstance(e, HTTPException):
        code = e.code
        name = e.name
        description = e.description
    error_details = {"code": code, "name": name, "description": description}
    return jsonify({'error': error_details})

# Register http exceptions to error handler
for code in http_exceptions:
    app.register_error_handler(code, handle_error)
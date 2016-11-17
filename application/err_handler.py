
from flask import logging
from .app import *
from werkzeug.exceptions import HTTPException

from .facilities import json_response

@app.errorhandler(Exception)
def handle_error(e):

    return json_response(str(e))

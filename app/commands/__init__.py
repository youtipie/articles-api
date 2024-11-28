from flask import Blueprint

bp = Blueprint("commands", __name__)

from . import routes

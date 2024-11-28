from flask import Blueprint

bp = Blueprint("article", __name__, url_prefix="/article")

from . import routes

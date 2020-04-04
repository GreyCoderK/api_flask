from flask import Blueprint

bp = Blueprint('api', __name__)

from . import user, errors, tokens, article, menu_vertical, type_article, type_user
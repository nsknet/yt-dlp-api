from flask import Blueprint, jsonify

bp = Blueprint('index', __name__)

@bp.app_errorhandler(404)
def page_not_found(e):
    return '404', 404

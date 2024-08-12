from controllers.customerController import get_token
from flask import Blueprint

token_blueprint = Blueprint('token_bp', __name__)
token_blueprint.route('/', methods=["POST"])(get_token)
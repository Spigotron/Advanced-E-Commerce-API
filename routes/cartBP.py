from controllers.cartController import add_to_cart, empty_cart, remove_from_cart, view_cart
from flask import Blueprint

cart_blueprint = Blueprint('cart_bp', __name__)
cart_blueprint.route('/', methods=['POST'])(add_to_cart)
cart_blueprint.route('/', methods=['GET'])(view_cart)
cart_blueprint.route('/<cart_id>', methods=['DELETE'])(remove_from_cart)
cart_blueprint.route('/', methods=['DELETE'])(empty_cart)
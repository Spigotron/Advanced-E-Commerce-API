from controllers.orderController import delete_order, find_all, get_order, save
from flask import Blueprint

order_blueprint = Blueprint('order_bp', __name__)
order_blueprint.route('/', methods=['POST'])(save)
order_blueprint.route('/', methods=['GET'])(find_all)
order_blueprint.route('/<order_id>', methods=['GET'])(get_order)
order_blueprint.route('/<order_id>', methods=['DELETE'])(delete_order)
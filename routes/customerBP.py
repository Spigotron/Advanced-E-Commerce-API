from controllers.customerController import delete_customer, find_all, get_customer, save, update_customer
from flask import Blueprint

customer_blueprint = Blueprint("customer_bp", __name__)
customer_blueprint.route('/', methods=['POST'])(save)
customer_blueprint.route('/', methods=['GET'])(find_all)
customer_blueprint.route('/<customer_id>', methods=['GET'])(get_customer)
customer_blueprint.route('/<customer_id>', methods=['PUT'])(update_customer)
customer_blueprint.route('/<customer_id>', methods=['DELETE'])(delete_customer)
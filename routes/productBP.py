from controllers.productController import delete_product, find_all, get_product, save, update_product
from flask import Blueprint

product_blueprint = Blueprint('product_bp', __name__)
product_blueprint.route('/', methods=['POST'])(save)
product_blueprint.route('/', methods=['GET'])(find_all)
product_blueprint.route('/<product_id>', methods=['GET'])(get_product)
product_blueprint.route('/<product_id>', methods=['PUT'])(update_product)
product_blueprint.route('/<product_id>', methods=['DELETE'])(delete_product)
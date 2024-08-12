from auth import token_auth
from caching import cache
from flask import request, jsonify
from marshmallow import ValidationError
from schemas.productSchema import product_input_schema, product_output_schema, products_schema, product_update_schema
from services import productService

@cache.cached(timeout=60)

@token_auth.login_required
def save():
    try:
        product_data = product_input_schema.load(request.json)
        new_product = productService.save(product_data)
        return product_output_schema.jsonify(new_product), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@token_auth.login_required
def update_product(product_id):
    try:
        product_data = product_update_schema.load(request.json)
        updated_product = productService.update_product(product_id, product_data)
        return product_output_schema.jsonify(updated_product), 200
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@token_auth.login_required
def delete_product(product_id):
    try:
        productService.delete_product(product_id)
        return '', 204
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def find_all():
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    search_term = args.get('search')
    products = productService.find_all(page, per_page, search_term)
    return products_schema.jsonify(products)

def get_product(product_id):
    product = productService.get_product(product_id)
    if product:
        return product_output_schema.jsonify(product)
    else:
        resp = {
            "status": "error",
            "message": f'A product with ID {product_id} does not exist'
        }
        return jsonify(resp), 404
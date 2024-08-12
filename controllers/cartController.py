from auth import token_auth
from caching import cache
from flask import request, jsonify
from marshmallow import ValidationError
from schemas.cartSchema import cart_input_schema, cart_output_schema, cart_schema, carts_schema
from services import cartService

@cache.cached(timeout=60)

@token_auth.login_required
def add_to_cart():
    try:
        raw_data = request.json
        cart_data = cart_schema.load(raw_data)
        cart_save = cartService.add_to_cart(cart_data)
        return cart_schema.jsonify(cart_save), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as err:
        return jsonify({'Error': str(err)}), 400

def view_cart():
    carts = cartService.view_cart()
    return carts_schema.jsonify(carts)

def remove_from_cart(cart_id):
    try:
        cartService.remove_from_cart(cart_id)
        return '', 204
    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 404
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    
@token_auth.login_required
def empty_cart():
    try:
        cartService.empty_cart()
        return jsonify({"Success": "Cart Emptied"}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
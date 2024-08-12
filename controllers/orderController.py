from auth import token_auth
from caching import cache
from flask import request, jsonify
from marshmallow import ValidationError
from schemas.orderSchema import order_input_schema, order_output_schema, order_schema, orders_schema
from services import orderService

@cache.cached(timeout=60)

@token_auth.login_required
def save():
    try:
        raw_data = request.json
        logged_in_user = token_auth.current_user()
        raw_data['customer_id'] = logged_in_user.id
        order_data = order_schema.load(raw_data)
        order_save = orderService.save(order_data)
        return order_schema.jsonify(order_save), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as err:
        return jsonify({'error': str(err)}), 400

def find_all():
    orders = orderService.find_all()
    return orders_schema.jsonify(orders)

def get_order(order_id):
    order = orderService.get_order(order_id)
    if order:
        return order_output_schema.jsonify(order)
    else:
        resp = {
            "status": "error",
            "message": f'A order with ID {order_id} does not exist'
        }
        return jsonify(resp), 404
    
@token_auth.login_required
def delete_order(order_id):
    try:
        orderService.delete_order(order_id)
        return '', 204
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
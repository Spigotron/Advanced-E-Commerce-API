from auth import token_auth
from caching import cache
from flask import request, jsonify
from marshmallow import ValidationError
from schemas.customerSchema import customer_input_schema, customer_login_schema, customer_output_schema, customers_schema, customer_update_schema
from services import customerService

@cache.cached(timeout=60)

def save():
    try:
        customer_data = customer_input_schema.load(request.json)
        new_customer = customerService.save(customer_data)
        return customer_output_schema.jsonify(new_customer), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return jsonify({"Error": str(e)}), 500

@cache.cached(timeout=60)

@token_auth.login_required
def update_customer(customer_id):
    try:
        customer_data = customer_update_schema.load(request.json)
        updated_customer = customerService.update_customer(customer_id, customer_data)
        return customer_output_schema.jsonify(updated_customer), 200
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as ve:
        return jsonify({"Error": str(ve)}), 404
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    
@token_auth.login_required
def delete_customer(customer_id):
    try:
        customerService.delete_customer(customer_id)
        return '', 204
    except ValueError as ve:
        return jsonify({"Error": str(ve)}), 404
    except Exception as e:
        return jsonify({"Error": str(e)}), 500

def find_all():
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    customers = customerService.find_all(page, per_page)
    return customers_schema.jsonify(customers), 200

def get_token():
    try:
        customer_data = customer_login_schema.load(request.json)
        token = customerService.get_token(customer_data['username'], customer_data['password'])
        if token:
            resp = {
                "Status": "Success",
                "Success": "You have successfully authenticated yourself",
                "Token": token
            }
            return jsonify(resp), 200
        else:
            resp = {
                "Status": "Error",
                "Message": "Username and/or password is incorrect"
            }
            return jsonify(resp), 401
    except ValidationError as err:
        return jsonify(err.messages), 400

def get_customer(customer_id):
    customer = customerService.get_customer(customer_id)
    if customer:
        return customer_output_schema.jsonify(customer)
    else:
        resp = {
            "status": "error",
            "message": f'A customer with ID {customer_id} does not exist'
        }
        return jsonify(resp), 404
from marshmallow import fields
from schemas import ma

class CustomerSchema(ma.Schema):
    id = fields.Integer(required=False)
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)

customer_input_schema = CustomerSchema()
customer_login_schema = CustomerSchema(only=["username", "password"])
customer_output_schema = CustomerSchema(exclude=["password"],)
customers_schema = CustomerSchema(many=True, exclude=["password"])
customer_update_schema = CustomerSchema(exclude=['password', 'username'])
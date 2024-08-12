from marshmallow import fields
from schemas import ma

class OrderSchema(ma.Schema):
    id = fields.Integer(required=False)
    date = fields.Date(required=False)
    customer_id = fields.Integer(required=True)
    products = fields.List(fields.Integer(), required=True)

order_input_schema = OrderSchema()
order_output_schema = OrderSchema()
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
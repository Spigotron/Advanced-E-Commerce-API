from marshmallow import fields
from schemas import ma

class CartSchema(ma.Schema):
    id = fields.Integer(required=False)
    item_name = fields.String(required=True)
    item_price = fields.Integer(required=True)
    item_quantity = fields.Integer(required=True)

cart_input_schema = CartSchema()
cart_output_schema = CartSchema()
cart_schema = CartSchema()
carts_schema = CartSchema(many=True)
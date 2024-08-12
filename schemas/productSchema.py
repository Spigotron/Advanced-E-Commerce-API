from marshmallow import fields
from schemas import ma

class ProductSchema(ma.Schema):
    id = fields.Integer(required=False)
    name = fields.String(required=True)
    price = fields.Integer(required=True)

product_input_schema = ProductSchema()
product_output_schema = ProductSchema()
products_schema = ProductSchema(many=True)
product_update_schema = ProductSchema()
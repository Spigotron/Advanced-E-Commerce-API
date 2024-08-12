from caching import cache
from database import db, migrate
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from limiter import limiter
from models.cart import Cart
from models.customer import Customer
from models.order import Order
from models.product import Product
from models.role import Role
from routes.cartBP import cart_blueprint
from routes.customerBP import customer_blueprint
from routes.orderBP import order_blueprint
from routes.productBP import product_blueprint
from routes.tokenBP import token_blueprint
from schemas import ma

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': 'CT E-Commerce'}
)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    blueprint_config(app)
    config_rate_limit()
    return app

def blueprint_config(app):
    app.register_blueprint(customer_blueprint, url_prefix='/customers')
    app.register_blueprint(product_blueprint, url_prefix='/products')
    app.register_blueprint(order_blueprint, url_prefix='/orders')
    app.register_blueprint(token_blueprint, url_prefix='/token')
    app.register_blueprint(cart_blueprint, url_prefix='/cart')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

def config_rate_limit():
    limiter.limit("100 per day")(customer_blueprint)
    limiter.limit("100 per day")(product_blueprint)
    limiter.limit("100 per day")(cart_blueprint)
    limiter.limit("100 per day")(order_blueprint)
    limiter.limit("100 per day")(token_blueprint)

if __name__ == "__main__":
    app = create_app('DevelopmentConfig')
    app.run(debug=True, port=8888)
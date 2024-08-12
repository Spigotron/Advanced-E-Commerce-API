from circuitbreaker import circuit
from database import db
from models.product import Product
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.util import encode_token
    
def save(product_data):
    with Session(db.engine) as session:
        with session.begin():
            product_query = select(Product).where(Product.name == product_data['name'])
            product_check = session.execute(product_query).scalars().first()
            if product_check is not None:
                raise ValueError("product with that name already exists")
            new_product = Product(name=product_data['name'], price=product_data['price'])
            session.add(new_product)
            session.commit()
        session.refresh(new_product)
        return new_product
    
def find_all(page=1, per_page=10, search_term=None):
    query = db.select(Product)
    if search_term:
        query = query.where(Product.name.ilike(f"%{search_term}%"))
    query = query.limit(per_page).offset((page-1)*per_page)
    products = db.session.execute(query).scalars().all()
    return products
    
def update_product(product_id, product_data):
    with Session(db.engine) as session:
        with session.begin():
            product = session.get(Product, product_id)
            if product is None:
                raise ValueError(f'Product with ID {product_id} does not exist')
            product.name = product_data.get('name', product.name)
            product.price = product_data.get('price', product.price)
            session.commit()
        session.refresh(product)
        return product
    
def delete_product(product_id):
    with Session(db.engine) as session:
        with session.begin():
            product = session.get(Product, product_id)
            if product is None:
                raise ValueError(f'product with ID {product_id} does not exist')
            else:
                print("Success: product Deleted")
            session.delete(product)
            session.commit()

def get_product(product_id):
    return db.session.get(Product, product_id)
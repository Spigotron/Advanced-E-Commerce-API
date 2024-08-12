from database import db
from models.customer import Customer
from models.order import Order
from models.product import Product
from sqlalchemy import select
from sqlalchemy.orm import Session

def save(order_data):
    with Session(db.engine) as session:
        with session.begin():
            order_query = select(Order).where(Order.date == order_data['date'])
            order_check = session.execute(order_query).scalars().first()
            if order_check is not None:
                raise ValueError("Order with that ID already exists")
            new_order = Order(date=order_data['date'], customer_id=order_data['customer_id'], products=order_data['products'])
            session.add(new_order)
            session.commit()
        session.refresh(new_order)
        return new_order
    
def find_all():
    query = select(Order)
    orders = db.session.execute(query).scalars().all()
    return orders

def get_order(order_id):
    return db.session.get(Order, order_id)

def delete_order(order_id):
    with Session(db.engine) as session:
        with session.begin():
            order = session.get(Order, order_id)
            if order is None:
                raise ValueError(f'order with ID {order_id} does not exist')
            else:
                print("Success: order Deleted")
            session.delete(order)
            session.commit()
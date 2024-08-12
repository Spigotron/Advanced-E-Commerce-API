from database import db
from models.cart import Cart
from models.customer import Customer
from models.order import Order
from models.product import Product
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

def add_to_cart(cart_data):
    with Session(db.engine) as session:
        with session.begin():
            cart_query = select(Cart).where(Cart.item_name == cart_data['item_name'])
            cart_check = session.execute(cart_query).scalars().first()
            if cart_check is not None:
                raise ValueError("Item with that ID already exists")
            new_item = Cart(item_name=cart_data['item_name'], item_price=cart_data['item_price'], item_quantity=cart_data['item_quantity'])
            session.add(new_item)
            session.commit()
        session.refresh(new_item)
        return new_item
    
def view_cart():
    query = select(Cart)
    carts = db.session.execute(query).scalars().all()
    return carts

def remove_from_cart(cart_id):
    with Session(db.engine) as session:
        with session.begin():
            cart = session.get(Cart, cart_id)
            if cart is None:
                raise ValueError(f'Item with ID {cart_id} does not exist')
            else:
                print("Success: Item Deleted")
            session.delete(cart)
            session.commit()

def empty_cart():
    try:
        with Session(db.engine) as session:
            with session.begin():
                query = select(Cart)
                cart_items = session.execute(query).scalars().all()
                if not cart_items:
                    print("The cart is already empty.")
                    return
                for item in cart_items:
                    session.delete(item)
                session.commit()
                print("Success: All items deleted from the cart")
    except SQLAlchemyError as e:
        print(f"Error: {str(e)}")
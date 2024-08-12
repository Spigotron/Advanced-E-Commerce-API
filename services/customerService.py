from circuitbreaker import circuit
from database import db
from models.customer import Customer
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.util import encode_token
from werkzeug.security import check_password_hash, generate_password_hash

def fallback_func(customer_data):
    print('The fallback function is being executed')
    return None

def save(customer_data):
    with Session(db.engine) as session:
        with session.begin():
            customer_query = select(Customer).where(Customer.username == customer_data['username'])
            customer_check = session.execute(customer_query).scalars().first()
            if customer_check is not None:
                raise ValueError("Customer with that username already exists")
            new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'], username=customer_data['username'], password=generate_password_hash(customer_data['password']))
            session.add(new_customer)
            session.commit()
        session.refresh(new_customer)
        return new_customer
    
def find_all(page=1, per_page=10):
    query = db.select(Customer).offset((page-1) * per_page).limit(per_page)
    customers = db.session.execute(query).scalars().all()
    return customers
    
def update_customer(customer_id, customer_data):
    with Session(db.engine) as session:
        with session.begin():
            customer = session.get(Customer, customer_id)
            if customer is None:
                raise ValueError(f'Customer with ID {customer_id} does not exist')
            customer.name = customer_data.get('name', customer.name)
            customer.email = customer_data.get('email', customer.email)
            customer.phone = customer_data.get('phone', customer.phone)
            session.commit()
        session.refresh(customer)
        return customer
    
def delete_customer(customer_id):
    with Session(db.engine) as session:
        with session.begin():
            customer = session.get(Customer, customer_id)
            if customer is None:
                raise ValueError(f'Customer with ID {customer_id} does not exist')
            else:
                print("Success: Customer Deleted")
            session.delete(customer)
            session.commit()

def get_token(username, password):
    query = db.select(Customer).where(Customer.username == username)
    customer = db.session.execute(query).scalars().first()
    if customer is not None and check_password_hash(customer.password, password):
        auth_token = encode_token(customer.id)
        return auth_token
    else:
        return None

def get_customer(customer_id):
    return db.session.get(Customer, customer_id)
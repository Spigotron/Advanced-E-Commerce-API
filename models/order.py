from database import Base, db
from models.order_product import order_product
from sqlalchemy.orm import Mapped, mapped_column
from typing import List
import datetime

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey("customers.id"), nullable = False)
    products: Mapped[List["Product"]] = db.relationship(secondary=order_product)
    item_quantity: Mapped[int] = mapped_column(db.Integer, nullable=False, default=1)
    date: Mapped[datetime.date] = mapped_column(db.Date, nullable=False, default=lambda : datetime.datetime.date(datetime.datetime.now()))
    customer: Mapped["Customer"]=db.relationship(back_populates="orders")
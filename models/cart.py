from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List

class Cart(Base):
    __tablename__ = "cart"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    item_quantity: Mapped[int] = mapped_column(db.Integer, nullable=False, default=1)
    customer=db.relationship("Customer", back_populates="cart_items")
    product=db.relationship("Product", back_populates="cart_items")
from database import Base, db
from models.order_product import order_product
from sqlalchemy.orm import Mapped, mapped_column
from typing import List

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)
    cart_items: Mapped[List["Cart"]]=db.relationship(back_populates="product")

    def __repr__(self):
        return f"<Product {self.id}|{self.name}>"
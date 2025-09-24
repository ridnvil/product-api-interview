from sqlalchemy import Column, Integer, String, Numeric

from config.base import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, default=0)

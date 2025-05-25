from sqlalchemy import Column, Integer, String, ForeignKey, Float
from app.db.base import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=False)
    size = Column(String, nullable=False)

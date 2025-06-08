from sqlalchemy import Column, Integer, String, ForeignKey, Float, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    style = Column(String)
    description = Column(String)

    variants = relationship('Variant', back_populates='product', cascade='all, delete-orphan')  # ✅


class Variant(Base):
    __tablename__ = 'variant'

    id = Column(Integer, primary_key= True)
    product_id = Column(Integer,ForeignKey('products.id', ondelete='CASCADE'))
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=False)
    sizes = relationship("SizeInfo", back_populates="variant", cascade="all, delete-orphan")

    product = relationship('Product', back_populates='variants')

class SizeInfo(Base):
    __tablename__ = "size_info"
    id = Column(Integer, primary_key=True)
    variant_id = Column(Integer, ForeignKey('variant.id', ondelete="CASCADE"))
    size = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    variant = relationship("Variant", back_populates="sizes")


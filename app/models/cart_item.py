from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db.base import Base


class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    variant_id = Column(Integer, ForeignKey('variant.id'), index=True)
    quantity = Column(Integer, default=1, nullable=False)
    size = Column(Float, nullable=False)
    variant = relationship("Variant")

from typing import Optional

from pydantic import BaseModel
from app.schemas.product import ProductRead
class CartItem(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItem):
    pass

class CartItemUpdate(BaseModel):
    quantity: int
    product_id: Optional[int] = None

    model_config = {"from_attributes": True}

class CartItemRead(BaseModel):
    id: int
    product: ProductRead
    quantity: int

    model_config = {"from_attributes": True}
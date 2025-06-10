from typing import Optional

from pydantic import BaseModel
from app.schemas.product import VariantRead


# class CartItem(BaseModel):
#     product_id: int
#     quantity: int

class CartItemCreate(BaseModel):
    variant_id: int
    quantity: int
    size: float
    model_config = {"from_attributes": True}
class CartItemUpdate(BaseModel):
    quantity: int
    model_config = {"from_attributes": True}

class CartItemRead(BaseModel):
    id: int
    variant: VariantRead
    quantity: int
    size: float
    computed_price: float

    model_config = {"from_attributes": True}
from typing import Optional

from pydantic import BaseModel
from app.schemas.product import VariantRead


class CartItem(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(BaseModel):
    variant_id: int
    quantity: int


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemRead(BaseModel):
    variant: VariantRead
    quantity: int

    model_config = {"from_attributes": True}
from typing import List, Optional

from pydantic import BaseModel



class VariantBase(BaseModel):

    price: float
    image_url: str
    size: float
    quantity: int

class VariantCreate(VariantBase):
    pass

class VariantRead(VariantBase):

    id: int
    model_config = {"from_attributes": True}
class ProductBase(BaseModel):

    name: str
    brand: str
    style: Optional[str] = None
    description: Optional[str] = None



class ProductCreate(ProductBase):
    variants: List[VariantCreate]

class ProductRead(ProductBase):

    id: int
    variants: List[VariantRead]
    model_config = {"from_attributes": True}
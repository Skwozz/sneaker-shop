from typing import List, Optional

from pydantic import BaseModel


class SizeInfo(BaseModel):
    size: float
    quantity: int

class SizeInfoRead(BaseModel):
    id: int
    size: float
    quantity: int
    model_config = {"from_attributes": True}


class VariantUpdate(BaseModel):
    price: float
    image_url: str
    sizes: List[SizeInfo]
class VariantBase(BaseModel):

    price: float
    image_url: str
    sizes: List[SizeInfo]

class VariantCreate(VariantBase):
    price: float
    image_url: str
    sizes: List[SizeInfo]
    model_config = {"from_attributes": True}

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
    model_config = {"from_attributes": True}

class ProductRead(ProductBase):

    id: int
    variants: List[VariantRead]
    model_config = {"from_attributes": True}

class ProductUpdate(BaseModel):
    name: str
    brand: str
    style: Optional[str] = None
    description: Optional[str] = None

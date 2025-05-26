from pydantic import BaseModel

class ProductBase(BaseModel):

    name: str
    brand: str
    price: float
    image_url: str
    size: str


class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):

    id: int
    model_config = {"from_attributes": True}
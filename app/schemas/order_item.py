from pydantic import BaseModel

from app.schemas.product import ProductRead


class OrderItemBase(BaseModel):
    order_id: int
    quantity: int
    product: ProductRead
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemRead(OrderItemBase):
    id: int

    class Config:
        orm_mode = True

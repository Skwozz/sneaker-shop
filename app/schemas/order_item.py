from pydantic import BaseModel

from app.schemas.product import ProductRead


class OrderItemRead(BaseModel):
    id: int
    quantity: int
    price: float
    product: ProductRead

    model_config = {"from_attributes": True}

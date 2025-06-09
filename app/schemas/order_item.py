from pydantic import BaseModel

from app.schemas.product import ProductRead, VariantRead


class OrderItemRead(BaseModel):
    id: int
    quantity: int
    price: float
    variant: VariantRead

    model_config = {"from_attributes": True}

class OrderItemCreate(BaseModel):
    variant_id: int
    size: float
    quantity: int
    price: float


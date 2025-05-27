from datetime import datetime

from pydantic import BaseModel

from app.schemas.order_item import OrderItemRead


class OrderBase(BaseModel):
    id: int
    created_at: datetime
    order_items: list[OrderItemRead]

    model_config = {"from_attributes": True}


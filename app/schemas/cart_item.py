from pydantic import BaseModel
from app.schemas.product import ProductRead
class CartItem(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItem):
    pass



class CartItemRead(BaseModel):
    id: int
    product: ProductRead
    quantity: int

    model_config = {"from_attributes": True}
from pydantic import BaseModel

class CartBase(BaseModel):
    user_id: int

class CartCreate(CartBase):
    pass

class CartRead(CartBase):
    id: int

    class Config:
        orm_mode = True

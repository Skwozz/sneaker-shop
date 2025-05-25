from pydantic import BaseModel

class OrderBase(BaseModel):
    user_id: int
    status: str = "pending"

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int

    class Config:
        orm_mode = True

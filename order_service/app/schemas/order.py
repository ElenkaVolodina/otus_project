from pydantic import BaseModel


class OrderCreate(BaseModel):
    address: str
    count: int
    status: str = 'created'


class Order(OrderCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True

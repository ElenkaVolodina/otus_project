from pydantic import BaseModel


class OrderCreate(BaseModel):
    flight_id: int
    order_id: int
    status: str = 'created'


class Order(OrderCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True

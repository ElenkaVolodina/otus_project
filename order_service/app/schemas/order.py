import datetime

from pydantic import BaseModel


class OrderCreate(BaseModel):
    count: int
    hotel_id: int
    flight_id: int
    country_id: int
    price: float
    date_from: datetime.date
    date_to: datetime.date
    status: str = 'created'


class Order(OrderCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True

import datetime

from pydantic import BaseModel


class CatalogCreate(BaseModel):
    flight_id: int
    hotel_id: int
    country_id: int
    date_from: datetime.date
    date_to: datetime.date
    price: float


class Catalog(CatalogCreate):
    id: int

    class Config:
        orm_mode = True

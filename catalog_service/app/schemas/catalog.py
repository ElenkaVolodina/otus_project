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


class FilterCatalog(BaseModel):
    flight_id: int | None
    hotel_id: int | None
    country_id: int  | None
    date_from: datetime.date | None
    date_to: datetime.date | None
    price: float | None
import sqlalchemy
from sqlalchemy import Column, Integer, String, Date, Float

from sqlalchemy.orm import declarative_base

metadata = sqlalchemy.MetaData()

Base = declarative_base(metadata=metadata)


class CatalogOrm(Base):
    __tablename__ = "catalog"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer)
    flight_id = Column(Integer)
    country_id = Column(Integer)
    date_from = Column(Date)
    date_to = Column(Date)
    price = Column(Float)

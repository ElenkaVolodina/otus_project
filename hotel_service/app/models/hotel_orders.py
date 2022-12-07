import sqlalchemy
from sqlalchemy import Column, Integer, String

from sqlalchemy.orm import declarative_base

metadata = sqlalchemy.MetaData()

Base = declarative_base(metadata=metadata)


class HotelOrderOrm(Base):
    __tablename__ = "hotel_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer)
    user_id = Column(Integer)
    hotel_id = Column(Integer)
    status = Column(String)


class HotelIdempotentRequestOrm(Base):
    __tablename__ = "hotel_idempotent_request"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    order_id = Column(Integer)
    idempotent_key = Column(String)

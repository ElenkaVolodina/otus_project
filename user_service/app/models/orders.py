import sqlalchemy
from sqlalchemy import Column, Integer, String, Date, Boolean, Float

from sqlalchemy.orm import declarative_base

metadata = sqlalchemy.MetaData()

Base = declarative_base(metadata=metadata)


class OrderOrm(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    hotel_id = Column(Integer)
    flight_id = Column(Integer)
    country_id = Column(Integer)
    date_from = Column(Date)
    date_to = Column(Date)
    count = Column(Integer)
    status = Column(String)
    price = Column(Float)
    check_hotel = Column(Boolean, default=False)
    check_ticket = Column(Boolean, default=False)
    check_pyment = Column(Boolean, default=False)


class IdempotentRequestOrm(Base):
    __tablename__ = "idempotent_request"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    order_id = Column(Integer)
    idempotent_key = Column(String)

import sqlalchemy
from sqlalchemy import Column, Integer, String, Text

from sqlalchemy.orm import declarative_base

metadata = sqlalchemy.MetaData()

Base = declarative_base(metadata=metadata)


class OrderOrm(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    address = Column(Text)
    count = Column(Integer)
    status = Column(String)


class IdempotentRequestOrm(Base):
    __tablename__ = "idempotent_request"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    order_id = Column(Integer)
    idempotent_key = Column(String)

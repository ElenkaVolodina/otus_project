import sqlalchemy
from sqlalchemy import Column, Integer, String, Text

from sqlalchemy.orm import declarative_base

metadata = sqlalchemy.MetaData()

Base = declarative_base(metadata=metadata)


class NotifyOrderOrm(Base):
    __tablename__ = "notify_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer)
    user_id = Column(Integer)
    subject = Column(String)
    text = Column(Text)

import sqlalchemy
from sqlalchemy import Column, Integer, Float, Boolean

from sqlalchemy.orm import declarative_base

metadata = sqlalchemy.MetaData()

Base = declarative_base(metadata=metadata)



class PymentAccountUserOrm(Base):
    __tablename__ = "pyment_account_user"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    debit = Column(Float)


class PymentOrderOrm(Base):
    __tablename__ = "pyment_orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    order_id = Column(Integer)
    price = Column(Float)
    success = Column(Boolean, default=False)

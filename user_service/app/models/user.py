import sqlalchemy
from sqlalchemy import Column, Integer, String

from sqlalchemy.orm import declarative_base

metadata = sqlalchemy.MetaData()

Base = declarative_base(metadata=metadata)


class UserOrm(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    password = Column(String)

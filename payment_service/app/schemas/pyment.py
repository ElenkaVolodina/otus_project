from pydantic import BaseModel


class PymentOrderCreate(BaseModel):
    user_id: int
    order_id: int
    price: float
    success: bool


class PymentAccountUserCreate(BaseModel):
    user_id: int


class PymentAccountUserUpdate(BaseModel):
    money: float


class PymentAccountUser(PymentAccountUserCreate):
    id: int
    debit: int

    class Config:
        orm_mode = True

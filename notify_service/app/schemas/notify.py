from pydantic import BaseModel


class NotifyCreate(BaseModel):
    order_id: int
    user_id: int
    subject: str
    text: str


class Notify(NotifyCreate):
    id: int

    class Config:
        orm_mode = True

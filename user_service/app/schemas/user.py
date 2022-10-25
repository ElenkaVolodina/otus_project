from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str


class UserCreate(BaseUser):
    password: str
    password1: str


class UserUpdate(BaseModel):
    first_name: str | None
    last_name: str | None
    email: EmailStr | None
    phone: str | None


class User(BaseUser):
    id: int
    password: str

    class Config:
        orm_mode = True

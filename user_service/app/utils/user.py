from sqlalchemy import insert, delete, update
from sqlalchemy.future import select

from app.database import SessionLocal
from app.models import UserOrm
from app.schemas.user import UserCreate, UserUpdate


async def get_user_by_username(username: str):
    async with SessionLocal() as session:
        q = select(UserOrm).where((UserOrm.username == username))
        result = await session.execute(q)
        return result.scalars().first()


async def get_user(user_id):
    async with SessionLocal() as session:
        q = select(UserOrm).where((UserOrm.id == int(user_id)))
        result = await session.execute(q)
        return result.scalars().first()


async def get_users():
    async with SessionLocal() as session:
        q = select(UserOrm)
        result = await session.execute(q)
        return result.scalars()


async def create_user(user: UserCreate):
    async with SessionLocal() as session:
        async with session.begin():
            query = insert(UserOrm).values(
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone=user.phone,
                password=user.password,
            ).returning(UserOrm.id)
            last_record_id = await session.execute(query)
            return {**user.dict(), "id": last_record_id.scalars().first()}


async def delete_user(user_id: int):
    async with SessionLocal() as session:
        async with session.begin():
            q = delete(UserOrm).where((UserOrm.id == user_id))
            await session.execute(q)


async def update_user(user_id, user: UserUpdate):
    async with SessionLocal() as session:
        async with session.begin():
            values_dict = {k: v for k, v in user.dict().items() if v}
            q = update(UserOrm).where((UserOrm.id == int(user_id))).values(
                **values_dict
            )
            await session.execute(q)

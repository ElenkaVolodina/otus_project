from sqlalchemy import insert

from auth.database import SessionLocal
from auth.models import UserOrm
from auth.schemas.user import UserCreate


async def create_user(user: UserCreate):
    async with SessionLocal() as session:
        async with session.begin():
            query = insert(UserOrm).values(
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone=user.phone,
            ).returning(UserOrm.id)
            last_record_id = await session.execute(query)
            return {**user.dict(), "id": last_record_id.scalars().first()}

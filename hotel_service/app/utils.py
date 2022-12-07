from sqlalchemy import insert, select, update

from app.database import SessionLocal
from app.models import HotelOrderOrm, HotelIdempotentRequestOrm
from app.schemas.order import OrderCreate


async def create_order(order: OrderCreate, user_id: int):
    async with SessionLocal() as session:
        async with session.begin():
            query = insert(HotelOrderOrm).values(
                user_id=user_id,
                hotel_id=order.hotel_id,
                order_id=order.order_id,
                status=order.status,
            ).returning(HotelOrderOrm.id)
            last_record_id = await session.execute(query)
            return {**order.dict(), "id": last_record_id.scalars().first(), "user_id": user_id}


async def create_idempotent_request(idempotent_key: str, user_id: int, order_id: int):
    async with SessionLocal() as session:
        async with session.begin():
            obj = insert(HotelIdempotentRequestOrm).values(
                user_id=user_id,
                order_id=order_id,
                idempotent_key=idempotent_key,
            )
            await session.execute(obj)


async def get_order_by_idempotent_key(idempotent_key: str, user_id: int):
    async with SessionLocal() as session:
        q = select(HotelIdempotentRequestOrm).where(
            (HotelIdempotentRequestOrm.idempotent_key == idempotent_key),
            (HotelIdempotentRequestOrm.user_id == user_id),
        )
        result = await session.execute(q)
        return result.scalars().first()


async def get_order_by_id(order_id: int):
    async with SessionLocal() as session:
        order = select(HotelOrderOrm).where(
            (HotelOrderOrm.order_id == order_id),
        )
        result = await session.execute(order)
        return result.scalars().first()


async def update_order_status(order_id: int, status: str):
    async with SessionLocal() as session:
        async with session.begin():
            q = update(HotelOrderOrm).where((HotelOrderOrm.order_id == order_id)).values(
                status=status
            )
            await session.execute(q)

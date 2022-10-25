from sqlalchemy import insert, select

from app.database import SessionLocal
from app.models import OrderOrm, IdempotentRequestOrm
from app.schemas.order import OrderCreate


async def create_order(order: OrderCreate, user_id: int):
    async with SessionLocal() as session:
        async with session.begin():
            query = insert(OrderOrm).values(
                user_id=user_id,
                address=order.address,
                count=order.count,
                status=order.status,
            ).returning(OrderOrm.id)
            last_record_id = await session.execute(query)
            return {**order.dict(), "id": last_record_id.scalars().first(), "user_id": user_id}


async def create_idempotent_request(idempotent_key: str, user_id: int, order_id: int):
    async with SessionLocal() as session:
        async with session.begin():
            obj = insert(IdempotentRequestOrm).values(
                user_id=user_id,
                order_id=order_id,
                idempotent_key=idempotent_key,
            )
            await session.execute(obj)


async def get_order_by_idempotent_key(idempotent_key: str, user_id: int):
    async with SessionLocal() as session:
        q = select(IdempotentRequestOrm).where(
            (IdempotentRequestOrm.idempotent_key == idempotent_key),
            (IdempotentRequestOrm.user_id == user_id),
        )
        result = await session.execute(q)
        return result.scalars().first()


async def get_order_by_id(order_id: int):
    async with SessionLocal() as session:
        order = select(OrderOrm).where(
            (OrderOrm.id == order_id),
        )
        result = await session.execute(order)
        return result.scalars().first()

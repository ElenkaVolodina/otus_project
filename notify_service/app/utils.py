from sqlalchemy import insert, select

from app.database import SessionLocal
from app.models import NotifyOrderOrm
from app.schemas.notify import NotifyCreate


async def create_notify(notify: NotifyCreate, user_id: int):
    async with SessionLocal() as session:
        async with session.begin():
            query = insert(NotifyOrderOrm).values(
                user_id=user_id,
                order_id=notify.order_id,
                subject=notify.subject,
                text=notify.text,
            ).returning(NotifyOrderOrm.id)
            last_record_id = await session.execute(query)
            return {**notify.dict(), "id": last_record_id.scalars().first()}


async def get_notify_by_order_id(order_id: int):
    async with SessionLocal() as session:
        order = select(NotifyOrderOrm).where(
            (NotifyOrderOrm.order_id == order_id),
        )
        result = await session.execute(order)
        return result.scalars().all()


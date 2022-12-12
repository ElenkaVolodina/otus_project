from sqlalchemy import insert, select, update

from app.database import SessionLocal
from app.models import PymentAccountUserOrm, PymentOrderOrm
from app.schemas.pyment import PymentAccountUserCreate, PymentAccountUserUpdate, PymentOrderCreate

async def create_pyment_user_account(user_id: int):
    async with SessionLocal() as session:
        async with session.begin():
            query = insert(PymentAccountUserOrm).values(
                user_id=user_id,
                debit=0,
            )
            await session.execute(query)


async def update_pyment_user_account(user_account: PymentAccountUserUpdate, user_id: int):
    async with SessionLocal() as session:
        async with session.begin():
            q = update(PymentAccountUserOrm).where((PymentAccountUserOrm.user_id == user_id)).values(
                debit=PymentAccountUserOrm.debit + user_account.money
            )
            await session.execute(q)


async def get_pyment_user_account(user_id: int):
    async with SessionLocal() as session:
        user_account = select(PymentAccountUserOrm).where(
            (PymentAccountUserOrm.user_id == user_id),
        )
        result = await session.execute(user_account)
        return result.scalars().first()


async def create_pyment_order(user_id: int, order_id: int, price: float):
    async with SessionLocal() as session:
        async with session.begin():
            query = insert(PymentOrderOrm).values(
                user_id=user_id,
                order_id=order_id,
                price=price,
                success=True,
            )
            await session.execute(query)


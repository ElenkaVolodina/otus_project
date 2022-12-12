from sqlalchemy import insert

from app.database import SessionLocal
from app.models import CatalogOrm
from app.schemas.catalog import CatalogCreate


async def create_catalog(voucher: CatalogCreate):
    async with SessionLocal() as session:
        async with session.begin():
            query = insert(CatalogOrm).values(
                hotel_id=voucher.hotel_id,
                flight_id=voucher.flight_id,
                country_id=voucher.country_id,
                date_from=voucher.date_from,
                date_to=voucher.date_to,
                price=voucher.price,
            ).returning(CatalogOrm.id)
            last_record_id = await session.execute(query)
            return {**voucher.dict(), "id": last_record_id.scalars().first()}

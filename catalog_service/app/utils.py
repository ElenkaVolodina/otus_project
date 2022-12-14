from sqlalchemy import insert, select

from app.database import SessionLocal
from app.models import CatalogOrm
from app.schemas.catalog import CatalogCreate, FilterCatalog


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


async def filter_catalog(filters: FilterCatalog):
    query_filters = tuple()
    if filters.flight_id:
        query_filters += (CatalogOrm.flight_id == filters.flight_id,)
    if filters.country_id:
        query_filters += (CatalogOrm.country_id == filters.country_id,)
    if filters.hotel_id:
        query_filters += (CatalogOrm.hotel_id == filters.hotel_id,)
    async with SessionLocal() as session:
        results = select(CatalogOrm).where(*query_filters)
        result = await session.execute(results)
    return result.scalars().all()



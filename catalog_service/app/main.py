import asyncio

from fastapi import FastAPI, Request, HTTPException
from pydantic.schema import List

from app import utils
from app.rm_client import PikaClient
from app.schemas.catalog import Catalog, CatalogCreate, FilterCatalog


async def log_incoming_message(message: dict):
    """Method to do something meaningful with the incoming message"""
    await utils.create_catalog(CatalogCreate(**message))


app = FastAPI(
    title="OTUS HomeWork #8",
    version="1",
)
app.pika_client = PikaClient(log_incoming_message)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "OK"}


@app.post("/create_voucher", response_model=Catalog)
async def create_order(request: Request, catalog: CatalogCreate):
    db_catalog = await utils.create_catalog(catalog)
    return db_catalog


@app.get('/send-message')
async def send_message(request: Request):
    request.app.pika_client.send_message(
        {
            "date_from": "2023-01-31",
            "date_to": "2023-02-10",
            "flight_id": 123,
            "hotel_id": 321,
            "country_id": 3,
            "price": 1234567,
        }
    )
    return {"status": "ok"}



@app.post("/search", response_model=List[Catalog])
async def get_catalog(request: Request, catalog: FilterCatalog):
    db_catalogs = await utils.filter_catalog(catalog)
    return db_catalogs



@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task
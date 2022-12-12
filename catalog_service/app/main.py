import asyncio

from fastapi import FastAPI, Request, HTTPException

from app import utils
from app.rm_client import PikaClient
from app.schemas.catalog import Catalog, CatalogCreate

async def log_incoming_message(message: dict):
    """Method to do something meaningful with the incoming message"""
    print(message)
    await utils.create_catalog(**message)


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
    db_catalog = await utils.create_catalog(catalog=catalog)
    return db_catalog


# @app.get("/order/{order_id}/", response_model=Order)
# async def get_order(order_id: int):
#     db_order = await utils.get_order_by_id(order_id=order_id)
#     if db_order is None:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return db_order


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task
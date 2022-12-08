import asyncio

from fastapi import FastAPI, Request, HTTPException

from app import utils
from app.rm_client import PikaClient
from app.schemas.order import Order, OrderCreate

async def log_incoming_message(message: dict):
    """Method to do something meaningful with the incoming message"""
    order_id = message.get('order_id')
    status = message.get('status')
    if status == 'created':
        idempotent_key = message.get('idempotent_key')
        if not idempotent_key:
            return
        user_id = message.get('user_id')
        idempotent_request = await utils.get_order_by_idempotent_key(idempotent_key=idempotent_key, user_id=user_id)
        if idempotent_request:
            return
        hotel_id = message.get('hotel_id')
        order = OrderCreate(
            user_id=user_id,
            order_id=order_id,
            hotel_id=hotel_id,
            status='pending',
        )
        db_order = await utils.create_order(order=order, user_id=user_id)
        await utils.create_idempotent_request(idempotent_key=idempotent_key, user_id=user_id, order_id=db_order['id'])

        if int(hotel_id) == 11:
            app.pika_client.send_message(
                {
                    "order_id": order_id,
                    "status": "canceled"
                }
            )
    elif status == 'canceled':
        await utils.update_order_status(order_id=order_id, status='canceled')


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

@app.get("/order/{order_id}/", response_model=Order)
async def get_order(order_id: int):
    db_order = await utils.get_order_by_id(order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


# @app.get('/send-message')
# async def send_message(request: Request):
#     request.app.pika_client.send_message(
#         {
#             "order_id": 111,
#             "status": "created",
#             "idempotent_key": "idempotent_key",
#             "flight_id": 222,
#             "hotel_id": 222,
#             "user_id": 333,
#         }
#     )
#     return {"status": "ok"}


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task
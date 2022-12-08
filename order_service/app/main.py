import asyncio

from fastapi import FastAPI, Request, HTTPException

from app import order_utils
from app.schemas.order import Order, OrderCreate
from app.rm_client import PikaClient


async def log_incoming_message(message: dict):
    """Method to do something meaningful with the incoming message"""
    print(message)
    order_id = message.get('order_id')
    status = message.get('status')
    if status == 'canceled':
        await order_utils.update_order_status(order_id=order_id, status='canceled')


app = FastAPI(
    title="OTUS HomeWork #6",
    version="1",
)

app.pika_client = PikaClient(log_incoming_message)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "OK"}


@app.post("/create_order", response_model=Order)
async def create_user(request: Request, order: OrderCreate):
    idempotent_key = request.headers.get('Idempotency-Key')
    user_id = int(request.headers.get('x-user_id'))
    if not idempotent_key:
        raise HTTPException(status_code=400, detail="idempotent_key error")
    idempotent_request = await order_utils.get_order_by_idempotent_key(idempotent_key=idempotent_key, user_id=user_id)
    if idempotent_request:
        db_order = await order_utils.get_order_by_id(order_id=idempotent_request.order_id)
        return db_order
    db_order = await order_utils.create_order(order=order, user_id=user_id)
    await order_utils.create_idempotent_request(idempotent_key=idempotent_key, user_id=user_id, order_id=db_order['id'])
    request.app.pika_client.send_message(
        {
            "order_id": db_order['id'],
            "status": "created",
            "idempotent_key": idempotent_key,
            "hotel_id": order.hotel_id,
            "flight_id": order.flight_id,
            "user_id": user_id,
        }
    )
    return db_order

@app.get("/order/{order_id}/", response_model=Order)
async def get_order(order_id: int):
    db_order = await order_utils.get_order_by_id(order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order



@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task

# @app.get('/send-message')
# async def send_message(request: Request):
#     request.app.pika_client.send_message(
#         {
#             "order_id": 222,
#             "status": "created",
#             "idempotent_key": "idempotent_key_n",
#             "flight_id": 333,
#             "hotel_id": 444,
#             "user_id": 333
#         }
#     )
#     return {"status": "ok"}
#
#
# @app.get('/cancel')
# async def cancel(request: Request):
#     request.app.pika_client.send_message(
#         {
#             "order_id": 222,
#             "status": "canceled"
#         }
#     )
#     return {"status": "ok"}
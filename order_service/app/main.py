from fastapi import FastAPI, Request, HTTPException

from app import order_utils
from app.schemas.order import Order, OrderCreate

app = FastAPI(
    title="OTUS HomeWork #6",
    version="1",
)


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
    return db_order

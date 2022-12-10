import asyncio

from fastapi import FastAPI, Request, HTTPException

from app import utils
from app.rm_client import PikaClient
from app.schemas.pyment import PymentAccountUser, PymentAccountUserUpdate, PymentOrderCreate

async def log_incoming_message(message: dict):
    """Method to do something meaningful with the incoming message"""
    print(message)
    # order_id = message.get('order_id')
    status = message.get('status')
    user_id = message.get('user_id')
    if status == 'user_create':
        await utils.create_pyment_user_account(user_id)
    elif status == 'pyment_create':
        order_id = message.get('order_id')
        price = message.get('price')
        db_user_acc = await utils.get_pyment_user_account(user_id=user_id)
        if db_user_acc:
            if db_user_acc.debit < price:
                app.pika_client.send_message(
                    {
                        "order_id": order_id,
                        "user_id": user_id,
                        "status": "pyment_canceled"
                    }
                )
            else:
                await utils.create_pyment_order(user_id=user_id, order_id=order_id, price=price)
                await utils.update_pyment_user_account(PymentAccountUserUpdate(money=price * -1), user_id=user_id)
                app.pika_client.send_message(
                    {
                        "order_id": order_id,
                        "user_id": user_id,
                        "status": "pyment_accept"
                    }
                )


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

@app.get("/user/", response_model=PymentAccountUser)
async def get_pyment_account(request: Request):
    user_id = int(request.headers.get('x-user_id'))
    db_user_acc = await utils.get_pyment_user_account(user_id=user_id)
    if db_user_acc is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user_acc


@app.put('/put/')
async def put_money_pyment_account(request: Request, data: PymentAccountUserUpdate):
    user_id = int(request.headers.get('x-user_id'))
    db_user_acc = await utils.get_pyment_user_account(user_id=user_id)
    if db_user_acc is None:
        raise HTTPException(status_code=404, detail="User not found")
    await utils.update_pyment_user_account(data, user_id=user_id)


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task
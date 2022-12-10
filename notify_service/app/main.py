import asyncio

from fastapi import FastAPI, Request, HTTPException
from pydantic.schema import List

from app import utils
from app.rm_client import PikaClient
from app.schemas.notify import Notify, NotifyCreate

async def log_incoming_message(message: dict):
    """Method to do something meaningful with the incoming message"""
    order_id = message.get('order_id')
    status = message.get('status')
    user_id = message.get('user_id')
    if status == 'created':
        notify = NotifyCreate(
            user_id=user_id,
            order_id=order_id,
            subject='Создан новый заказ!',
            text=f'Добрый день! Создан заказ № {order_id}. Мы уже работаем над ним.',
        )
        await utils.create_notify(notify=notify, user_id=user_id)
    elif status == 'pyment_canceled':
        notify = NotifyCreate(
            user_id=user_id,
            order_id=order_id,
            subject='Не удачная оплата заказа!',
            text=f'Добрый день! На Вашем счете недостаточно средств для оплаты заказа № {order_id}. Заказ был отменен.',
        )
        await utils.create_notify(notify=notify, user_id=user_id)
    elif status == 'pyment_accept':
        notify = NotifyCreate(
            user_id=user_id,
            order_id=order_id,
            subject='Ваш заказ оплачен!',
            text=f'Добрый день! Ваш заказ № {order_id} успешно оплачен.',
        )
        await utils.create_notify(notify=notify, user_id=user_id)



app = FastAPI(
    title="OTUS HomeWork #9",
    version="1",
)
app.pika_client = PikaClient(log_incoming_message)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "OK"}

@app.get("/{order_id}/", response_model=List[Notify])
async def get_notify(order_id: int):
    db_notify = await utils.get_notify_by_order_id(order_id=order_id)
    if not db_notify:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_notify


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task
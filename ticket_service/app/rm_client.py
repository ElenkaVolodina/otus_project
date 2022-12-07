import json
import os
import uuid

import pika
from aio_pika import connect_robust


class PikaClient:

    def __init__(self, process_callable):
        self.publish_queue_name = os.getenv('PUBLISH_QUEUE', 'order_queue')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.getenv('RABBIT_HOST', '127.0.0.1'))
        )
        self.channel = self.connection.channel()
        self.publish_queue = self.channel.queue_declare(queue=self.publish_queue_name)
        self.callback_queue = self.publish_queue.method.queue
        self.response = None
        self.process_callable = process_callable

    async def consume(self, loop):
        """Setup message listener with the current running loop"""
        connection = await connect_robust(
            host=os.getenv('RABBIT_HOST', '127.0.0.1'),
            port=5672,
            loop=loop,
        )
        channel = await connection.channel()
        queue = await channel.declare_queue(os.getenv('CONSUME_QUEUE', 'ticket_order_queue'))
        await queue.consume(self.process_incoming_message, no_ack=True)
        return connection

    async def process_incoming_message(self, message):
        """Processing incoming message from RabbitMQ"""
        message.ack()
        body = message.body
        if body:
            try:
                await self.process_callable(json.loads(body))
            except Exception as e:
                print(body)
                print(e)

    def send_message(self, message: dict):
        """Method to publish message to RabbitMQ"""
        self.channel.basic_publish(
            exchange='my_orders',
            routing_key=self.publish_queue_name,
            body=json.dumps(message).encode()
    )
import json
import os

import pika


class PikaClient:

    def __init__(self):
        self.publish_queue_name = os.getenv('PUBLISH_QUEUE', 'user_queue')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.getenv('RABBIT_HOST', '127.0.0.1'),
                credentials=pika.credentials.PlainCredentials(
                    'admin', 'admin'
                ),
                heartbeat=0,
            )
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare('my_orders')
        self.channel.queue_declare(queue=os.getenv('CONSUME_QUEUE', 'pyment_order_queue'))
        self.channel.queue_bind(
            exchange='my_orders',
            queue=os.getenv('CONSUME_QUEUE', 'pyment_order_queue'),
            routing_key=os.getenv('PUBLISH_QUEUE', 'user_queue'),
        )
        self.publish_queue = self.channel.queue_declare(queue=self.publish_queue_name)
        self.callback_queue = self.publish_queue.method.queue
        self.response = None

    def send_message(self, message: dict):
        """Method to publish message to RabbitMQ"""
        self.channel.basic_publish(
            exchange='my_orders',
            routing_key=self.publish_queue_name,
            body=json.dumps(message).encode()
    )
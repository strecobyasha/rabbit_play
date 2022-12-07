import asyncio
import time
from typing import Callable

from aio_pika import Message, connect

from settings import settings


class Rabbit:

    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None
        self.queues = {}

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.prepare())

    async def connect(self):
        self.connection = await connect('amqp://guest:guest@localhost/')
        self.channel = await self.connection.channel()

    async def create_exchange(self, name: str):
        self.exchange = await self.channel.declare_exchange(name=name)

    async def create_queue(self, name: str):
        queue = await self.channel.declare_queue(name, durable=True)
        await queue.bind(exchange=self.exchange.name)

        delayed_queue = await self.channel.declare_queue(
            f'{name}{settings.delayed_suffix}',
            durable=True,
            arguments={
                'x-dead-letter-exchange': self.exchange.name,
                'x-dead-letter-routing-key': queue.name,
            })
        await delayed_queue.bind(exchange=self.exchange.name)
        self.queues.update({queue.name: queue, delayed_queue.name: delayed_queue})

    async def prepare(self):
        await self.connect()
        await self.create_exchange(settings.exchange_name)
        await self.create_queue(settings.queue_name)

    async def send(self, queue: str, message: bytes, expiration: int = 0):
        if expiration:
            print(f' [x] {int(time.perf_counter())} Sent delayed {message}')
            await self.exchange.publish(
                    Message(message, expiration=expiration),
                    routing_key=self.queues[f'{queue}{settings.delayed_suffix}'].name,
                )
        else:
            print(f' [x] {int(time.perf_counter())} Sent {message}')
            await self.exchange.publish(
                Message(message),
                routing_key=self.queues[queue].name,
            )

    async def receive(self, queue: str, callback: Callable):
        await self.queues[queue].consume(callback, no_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        await asyncio.Future()

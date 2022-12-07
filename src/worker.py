import asyncio
import time

from aio_pika.abc import AbstractIncomingMessage

from broker import Rabbit

from settings import settings

counter = 0


async def on_message(message: AbstractIncomingMessage):
    print(f' [x] {int(time.perf_counter())} Received {message.body}')
    global counter
    global rabbit
    counter += 1
    if counter == 2:
        await rabbit.send(queue=settings.queue_name, message=message.body, expiration=3)


if __name__ == '__main__':
    rabbit = Rabbit()
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(rabbit.receive(queue=settings.queue_name, callback=on_message))

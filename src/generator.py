import asyncio
import time

import orjson as orjson

from models import Message
from broker import Rabbit
from settings import settings


if __name__ == '__main__':
    rabbit = Rabbit()

    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)

    for _ in range(settings.messages_num):
        message = Message()
        loop.run_until_complete(
            rabbit.send(
                queue=settings.queue_name,
                message=orjson.dumps(message.dict()),
            ),
        )
        time.sleep(settings.sleep_time)

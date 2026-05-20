from aiokafka import AIOKafkaProducer
import json, asyncio

class KafkaLogger:
    def __init__(self, brokers: list[str], topic: str):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=brokers,
            value_serializer=lambda v: json.dumps(v).encode()
        )
        self._topic = topic
        self._ready = False

    async def start(self):
        await self._producer.start()
        self._ready = True
    async def stop(self):
        await self._producer.stop()

    async def _push(self, level: str, message: str, **ctx):
        if not self._ready:
            await self.start()
        await self._producer.send_and_wait(self._topic, {"level": level, "msg": message, "ctx": ctx})

    async def info(self, message: str, **context):
        await self._push("INFO", message, **context)
    async def error(self, message: str, **context):
        await self._push("ERROR", message, **context)

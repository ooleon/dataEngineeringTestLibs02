import redis.asyncio as redis
from domain.ports.repository import ItemRepository
from domain.entities import Item
from infrastructure.cache.base import CacheSerializerMixin

class RedisItemRepository(CacheSerializerMixin, ItemRepository):
    def __init__(self, url: str, db: int = 0):
        self._client = redis.from_url(url, db=db, decode_responses=True, socket_timeout=2.0)
        self._prefix = "item:redis:"

    async def save(self, item: Item) -> Item:
        await self._client.set(f"{self._prefix}{item.id}", self._to_payload(item))
        return item

    async def get_by_id(self, item_id: str) -> Item | None:
        raw = await self._client.get(f"{self._prefix}{item_id}")
        return self._from_payload(raw) if raw else None

    async def delete(self, item_id: str) -> bool:
        return bool(await self._client.delete(f"{self._prefix}{item_id}"))

    async def list_all(self) -> list[Item]:
        keys = await self._client.keys(f"{self._prefix}*")
        return [self._from_payload(d) for k in keys if (d := await self._client.get(k))]

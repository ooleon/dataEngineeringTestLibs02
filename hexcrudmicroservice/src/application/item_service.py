from domain.ports.repository import ItemRepository
from domain.ports.logger import LoggerPort
from domain.entities import Item

class ItemService:
    def __init__(self, repo: ItemRepository, logger: LoggerPort):
        self.repo = repo
        self.logger = logger

    async def create(self, item: Item) -> Item:
        await self.logger.info("item_created", item_id=item.id, name=item.name)
        return await self.repo.save(item)

    async def get(self, item_id: str) -> Item | None:
        return await self.repo.get_by_id(item_id)

    async def delete(self, item_id: str) -> bool:
        deleted = await self.repo.delete(item_id)
        if deleted:
            await self.logger.info("item_deleted", item_id=item_id)
        return deleted

    async def list_all(self) -> list[Item]:
        return await self.repo.list_all()

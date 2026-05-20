from domain.entities import Item

class CacheSerializerMixin:
    @staticmethod
    def _to_payload(item: Item) -> str:
        return item.model_dump_json()

    @staticmethod
    def _from_payload(raw: str) -> Item:
        return Item.model_validate_json(raw)
